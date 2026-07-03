//! Request client — sends requests and awaits responses.

use std::sync::{Arc, Mutex};
use uuid::Uuid;

use super::request::Request;
use super::request::Response;
use super::correlator::Correlator;
use super::cancellation::CancellationToken;

/// Client for sending requests through the IPC runtime.
#[derive(Clone)]
pub struct RequestClient {
    correlator: Correlator,
    cancellation_token: CancellationToken,
    sent_requests: Arc<Mutex<Vec<Request>>>,
    responses: Arc<Mutex<Vec<Response>>>,
}

impl RequestClient {
    pub fn new() -> Self {
        Self {
            correlator: Correlator::default(),
            cancellation_token: CancellationToken::new(),
            sent_requests: Arc::new(Mutex::new(Vec::new())),
            responses: Arc::new(Mutex::new(Vec::new())),
        }
    }

    /// Send a request and return the request handle.
    pub fn send_request(
        &self,
        sender: impl Into<String>,
        receiver: impl Into<String>,
        payload: serde_json::Value,
    ) -> Request {
        let mut request = Request::new(sender, receiver, payload);
        request.mark_sent();
        self.correlator.register_pending(*request.correlation_id());
        let mut sent = self.sent_requests.lock().unwrap();
        sent.push(request.clone());
        request
    }

    /// Record a response for a correlation ID.
    pub fn record_response(&self, response: Response) {
        self.responses.lock().unwrap().push(response.clone());
        self.correlator.record_response(response.clone());
        self.correlator.remove_pending(&response.correlation_id);
    }

    /// Await a response by correlation ID (blocking in reference impl).
    pub fn await_response(&self, correlation_id: &Uuid, _timeout_secs: u64) -> Option<Response> {
        // In the reference implementation, check the correlator
        if let Some(resp) = self.correlator.find_response(correlation_id) {
            return Some(resp);
        }
        // Check local responses
        let responses = self.responses.lock().unwrap();
        responses.iter().find(|r| &r.correlation_id == correlation_id).cloned()
    }

    /// Cancel all pending requests.
    pub fn cancel_all(&self) {
        self.cancellation_token.cancel();
        self.correlator.cleanup_expired(0);
    }

    /// Get sent request count.
    pub fn sent_count(&self) -> usize {
        let sent = self.sent_requests.lock().unwrap();
        sent.len()
    }

    /// Get response count.
    pub fn response_count(&self) -> usize {
        let responses = self.responses.lock().unwrap();
        responses.len()
    }
}

impl Default for RequestClient {
    fn default() -> Self {
        Self::new()
    }
}






