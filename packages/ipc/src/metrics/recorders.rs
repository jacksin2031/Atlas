//! Individual metric recorders for each IPC subsystem.

use std::sync::{Arc, Mutex};

/// Records serialization timing metrics.
#[derive(Clone, Default)]
pub struct SerializationTimeRecorder {
    times: Arc<Mutex<Vec<f64>>>,
}

impl SerializationTimeRecorder {
    pub fn record(&self, time_ms: f64) {
        let mut times = self.times.lock().unwrap();
        times.push(time_ms);
        if times.len() > 10000 {
            let excess = times.len() - 10000;
            times.drain(0..excess);
        }
    }

    pub fn average(&self) -> f64 {
        let times = self.times.lock().unwrap();
        if times.is_empty() {
            0.0
        } else {
            times.iter().sum::<f64>() / times.len() as f64
        }
    }
}

/// Records message latency metrics.
#[derive(Clone, Default)]
pub struct LatencyRecorder {
    latencies: Arc<Mutex<Vec<f64>>>,
}

impl LatencyRecorder {
    pub fn record(&self, latency_ms: f64) {
        let mut latencies = self.latencies.lock().unwrap();
        latencies.push(latency_ms);
        if latencies.len() > 10000 {
            let excess = latencies.len() - 10000;
            latencies.drain(0..excess);
        }
    }

    pub fn average(&self) -> f64 {
        let latencies = self.latencies.lock().unwrap();
        if latencies.is_empty() {
            0.0
        } else {
            latencies.iter().sum::<f64>() / latencies.len() as f64
        }
    }

    pub fn max(&self) -> f64 {
        let latencies = self.latencies.lock().unwrap();
        latencies.iter().cloned().fold(0.0, f64::max)
    }
}

/// Records queue size metrics.
#[derive(Clone, Default)]
pub struct QueueSizeRecorder {
    sizes: Arc<Mutex<Vec<usize>>>,
}

impl QueueSizeRecorder {
    pub fn record(&self, size: usize) {
        let mut sizes = self.sizes.lock().unwrap();
        sizes.push(size);
        if sizes.len() > 10000 {
            let excess = sizes.len() - 10000;
            sizes.drain(0..excess);
        }
    }

    pub fn current(&self) -> usize {
        let sizes = self.sizes.lock().unwrap();
        *sizes.last().unwrap_or(&0)
    }
}
