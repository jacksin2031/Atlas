//! Request server — handles incoming requests and sends responses.

use std::sync::{Arc, Mutex};
use uuid::Uuid;

use super::correlator::Correlator;
use super::request::Request;
use super::request::Response;

/// Server for handling incoming requests through the IPC runtime.
#[derive(Clone)]
pub struct RequestServer {
    correlator: Correlator,
    pending_requests: Arc<Mutex<Vec<Request>>>,
    responses: Arc<Mutex<Vec<Response>>>,
}

impl RequestServer {
    pub fn new() -> Self {
        Self {
            correlator: Correlator::default(),
            pending_requests: Arc::new(Mutex::new(Vec::new())),
            responses: Arc::new(Mutex::new(Vec::new())),
        }
    }

    /// Receive and queue a request.
    pub fn receive_request(&self, request: Request) {
        let mut pending = self.pending_requests.lock().unwrap();
        pending.push(request.clone());
        self.correlator.register_pending(*request.correlation_id());
    }

    /// Send a response for a request's correlation ID.
    pub fn send_response(&self, correlation_id: Uuid, result: serde_json::Value) {
        let response = Response::success(correlation_id, result);
        self.responses.lock().unwrap().push(response.clone());
        self.correlator.record_response(response);
    }

    /// Send an error response for a request's correlation ID.
    pub fn send_error_response(&self, correlation_id: Uuid, error: impl Into<String>) {
        let response = Response::error(correlation_id, error);
        self.responses.lock().unwrap().push(response.clone());
        self.correlator.record_response(response);
    }

    /// Get pending requests.
    pub fn pending_requests(&self) -> Vec<Request> {
        let pending = self.pending_requests.lock().unwrap();
        pending.clone()
    }

    /// Get all responses.
    pub fn responses(&self) -> Vec<Response> {
        let responses = self.responses.lock().unwrap();
        responses.clone()
    }

    /// Get pending count.
    pub fn pending_count(&self) -> usize {
        let pending = self.pending_requests.lock().unwrap();
        pending.len()
    }
}

impl Default for RequestServer {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_request_response_cycle() {
        let server = RequestServer::new();
        let client = crate::request_response::RequestClient::new();

        // Create a request
        let req = Request::new("client", "server", serde_json::json!({"action": "test}"}));
        server.receive_request(req.clone());

        // Send response
        server.send_response(*req.correlation_id(), serde_json::json!({"result": "ok}"}));

        // Forward server response to client (simulating IPC delivery)
        for resp in server.responses() {
            client.record_response(resp);
        }

        // Client receives response
        let resp = client.await_response(req.correlation_id(), 30);
        assert!(resp.is_some());
        assert!(resp.unwrap().is_success());
    }
}
