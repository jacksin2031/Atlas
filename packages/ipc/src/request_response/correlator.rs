//! Correlator - matches responses to requests by correlation ID.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use uuid::Uuid;
use super::request::Response;

/// Matches responses to their originating requests.
#[derive(Clone, Default)]
pub struct Correlator {
    pending: Arc<Mutex<HashMap<Uuid, std::time::Instant>>>,
    responses: Arc<Mutex<HashMap<Uuid, Response>>>,
}

impl Correlator {
    pub fn register_pending(&self, correlation_id: Uuid) {
        let mut pending = self.pending.lock().unwrap();
        pending.insert(correlation_id, std::time::Instant::now());
    }

    pub fn record_response(&self, response: Response) {
        let mut responses = self.responses.lock().unwrap();
        responses.insert(response.correlation_id, response);
    }

    pub fn find_response(&self, correlation_id: &Uuid) -> Option<Response> {
        let responses = self.responses.lock().unwrap();
        responses.get(correlation_id).cloned()
    }

    pub fn is_pending(&self, correlation_id: &Uuid) -> bool {
        let pending = self.pending.lock().unwrap();
        pending.contains_key(correlation_id)
    }

    pub fn remove_pending(&self, correlation_id: &Uuid) {
        let mut pending = self.pending.lock().unwrap();
        pending.remove(correlation_id);
    }

    pub fn pending_count(&self) -> usize {
        let pending = self.pending.lock().unwrap();
        pending.len()
    }

    pub fn cleanup_expired(&self, timeout_secs: u64) -> Vec<Uuid> {
        let _instant = std::time::Instant::now();
        let mut pending = self.pending.lock().unwrap();
        let mut expired = Vec::new();
        pending.retain(|corr_id, created_at| {
            if created_at.elapsed().as_secs() >= timeout_secs {
                expired.push(*corr_id);
                false
            } else {
                true
            }
        });
        expired
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_correlate_response() {
        let corr = Correlator::default();
        let id = Uuid::new_v4();
        corr.register_pending(id);
        assert!(corr.is_pending(&id));

        let response = Response::success(id, serde_json::json!({"data": "ok"}));
        corr.record_response(response);

        let found = corr.find_response(&id);
        assert!(found.is_some());
        assert!(found.unwrap().is_success());
    }

    #[test]
    fn test_cleanup_expired() {
        let corr = Correlator::default();
        let id = Uuid::new_v4();
        corr.register_pending(id);
        let expired = corr.cleanup_expired(0);
        assert_eq!(expired.len(), 1);
        assert!(!corr.is_pending(&id));
    }
}

