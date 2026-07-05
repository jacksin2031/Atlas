//! Deterministic priority queue for message routing.

use crate::message::{MessageEnvelope, MessagePriority};

/// A priority queue that delivers messages in priority order.
#[derive(Debug, Clone, Default)]
pub struct PriorityMessageQueue {
    queues: [Vec<MessageEnvelope>; 5],
    total_sent: u64,
    total_dropped: u64,
    max_size: usize,
}

impl PriorityMessageQueue {
    pub fn new(max_size: usize) -> Self {
        Self {
            queues: Default::default(),
            total_sent: 0,
            total_dropped: 0,
            max_size,
        }
    }

    pub fn enqueue(&mut self, msg: MessageEnvelope) -> bool {
        let priority_idx = msg.priority() as usize;
        if priority_idx >= 5 {
            return false;
        }
        let current_len: usize = self.queues.iter().map(|q| q.len()).sum();
        if current_len >= self.max_size {
            self.drop_lowest();
        }
        self.queues[priority_idx].push(msg);
        self.total_sent += 1;
        true
    }

    pub fn dequeue(&mut self) -> Option<MessageEnvelope> {
        for priority_idx in 0..5 {
            if let Some(msg) = self.queues[priority_idx].pop() {
                return Some(msg);
            }
        }
        None
    }

    pub fn peek(&self) -> Option<&MessageEnvelope> {
        for priority_idx in (0..5).rev() {
            if let Some(msg) = self.queues[priority_idx].last() {
                return Some(msg);
            }
        }
        None
    }

    pub fn preempt_if_needed(&mut self, threshold: usize) {
        let current_len: usize = self.queues.iter().map(|q| q.len()).sum();
        if current_len > threshold {
            self.drop_lowest_n(current_len - threshold);
        }
    }

    pub fn len_at_priority(&self, priority: MessagePriority) -> usize {
        self.queues[priority as usize].len()
    }

    pub fn len(&self) -> usize {
        self.queues.iter().map(|q| q.len()).sum()
    }

    pub fn is_empty(&self) -> bool {
        self.queues.iter().all(|q| q.is_empty())
    }

    pub fn stats(&self) -> QueueStats {
        QueueStats {
            total_enqueued: self.total_sent,
            total_dequeued: self.total_sent - self.len() as u64 + self.total_dropped,
            total_dropped: self.total_dropped,
            by_priority: self
                .queues
                .iter()
                .map(|q| q.len() as u64)
                .collect::<Vec<_>>()
                .try_into()
                .unwrap_or([0; 5]),
            current_size: self.len(),
            max_size: self.max_size,
        }
    }

    fn drop_lowest(&mut self) {
        for priority_idx in (0..5).rev() {
            if !self.queues[priority_idx].is_empty() {
                self.queues[priority_idx].pop();
                self.total_dropped += 1;
                return;
            }
        }
    }

    fn drop_lowest_n(&mut self, n: usize) {
        let mut remaining = n;
        for priority_idx in (0..5).rev() {
            if remaining == 0 {
                break;
            }
            let drop_count = std::cmp::min(remaining, self.queues[priority_idx].len());
            self.queues[priority_idx].truncate(self.queues[priority_idx].len() - drop_count);
            self.total_dropped += drop_count as u64;
            remaining -= drop_count;
        }
    }
}

/// Statistics for the priority queue.
#[derive(Debug, Clone)]
pub struct QueueStats {
    pub total_enqueued: u64,
    pub total_dequeued: u64,
    pub total_dropped: u64,
    pub by_priority: [u64; 5],
    pub current_size: usize,
    pub max_size: usize,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::message::{MessageHeader, MessageMetadata, MessagePayload, MessageType};

    fn make_msg(priority: MessagePriority) -> MessageEnvelope {
        MessageEnvelope {
            header: MessageHeader::new("sender", "receiver", MessageType::Request, 60),
            payload: MessagePayload::new(serde_json::json!({"p": priority as u8})).unwrap(),
            metadata: MessageMetadata::default().with_priority(priority),
        }
    }

    #[test]
    fn test_priority_order() {
        let mut q = PriorityMessageQueue::new(100);
        let low = make_msg(MessagePriority::Low);
        let critical = make_msg(MessagePriority::Critical);
        q.enqueue(low);
        q.enqueue(critical);
        let first = q.dequeue().unwrap();
        assert_eq!(first.metadata.priority, MessagePriority::Critical);
    }

    #[test]
    fn test_empty_queue_returns_none() {
        let mut q = PriorityMessageQueue::new(100);
        assert!(q.dequeue().is_none());
        assert!(q.peek().is_none());
        assert!(q.is_empty());
    }

    #[test]
    fn test_queue_stats() {
        let mut q = PriorityMessageQueue::new(10);
        q.enqueue(make_msg(MessagePriority::High));
        q.enqueue(make_msg(MessagePriority::Low));
        q.dequeue();
        let stats = q.stats();
        assert_eq!(stats.total_enqueued, 2);
        assert_eq!(stats.current_size, 1);
    }
}
