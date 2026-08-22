//! Retry policy with configurable backoff strategies.

use serde::{Deserialize, Serialize};
use std::time::Duration;

/// Backoff strategies for retry.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum BackoffStrategy {
    /// Fixed interval between retries.
    Fixed { interval: Duration },
    /// Exponential backoff with optional jitter.
    Exponential {
        base: Duration,
        multiplier: f64,
        max_delay: Duration,
        jitter: bool,
    },
    /// Linear backoff.
    Linear { step: Duration, max_delay: Duration },
}

impl Default for BackoffStrategy {
    fn default() -> Self {
        Self::Exponential {
            base: Duration::from_millis(100),
            multiplier: 2.0,
            max_delay: Duration::from_secs(30),
            jitter: true,
        }
    }
}

/// Retry policy configuration.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RetryPolicy {
    /// Maximum number of retry attempts.
    pub max_attempts: u32,
    /// Backoff strategy.
    pub backoff: BackoffStrategy,
    /// Whether to retry on all errors.
    pub retry_on_all: bool,
    /// Specific error types to retry on.
    pub retry_on_errors: Vec<String>,
}

impl Default for RetryPolicy {
    fn default() -> Self {
        Self {
            max_attempts: 3,
            backoff: BackoffStrategy::default(),
            retry_on_all: true,
            retry_on_errors: Vec::new(),
        }
    }
}

impl RetryPolicy {
    /// Calculate the delay for a given attempt number.
    pub fn delay_for_attempt(&self, attempt: u32) -> Duration {
        match &self.backoff {
            BackoffStrategy::Fixed { interval } => *interval,
            BackoffStrategy::Exponential {
                base,
                multiplier,
                max_delay,
                jitter,
            } => {
                let mut delay = (*base).as_millis() as f64 * multiplier.powi(attempt as i32);
                if *jitter {
                    let seed = std::time::SystemTime::now()
                        .duration_since(std::time::UNIX_EPOCH)
                        .unwrap_or_default()
                        .subsec_nanos() as f64;
                    delay *= 0.5 + (seed % 1_000_000_000.0) / 1_000_000_000.0;
                }
                let delay = delay as u64;
                Duration::from_millis(if delay > max_delay.as_millis() as u64 {
                    max_delay.as_millis() as u64
                } else {
                    delay
                })
            }
            BackoffStrategy::Linear { step, max_delay } => {
                let delay: u64 = (step.as_millis() as u64) * (attempt as u64);
                Duration::from_millis(if delay > max_delay.as_millis() as u64 {
                    max_delay.as_millis() as u64
                } else {
                    delay
                })
            }
        }
    }

    /// Check if a retry should be performed.
    pub fn should_retry(&self, attempt: u32) -> bool {
        attempt < self.max_attempts
    }

    /// Check if a specific error should trigger a retry.
    pub fn should_retry_error(&self, error_name: &str) -> bool {
        if self.retry_on_all {
            true
        } else {
            self.retry_on_errors.iter().any(|e| e == error_name)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fixed_backoff() {
        let policy = RetryPolicy {
            backoff: BackoffStrategy::Fixed {
                interval: Duration::from_secs(1),
            },
            ..RetryPolicy::default()
        };
        assert_eq!(policy.delay_for_attempt(0), Duration::from_secs(1));
        assert_eq!(policy.delay_for_attempt(5), Duration::from_secs(1));
    }

    #[test]
    fn test_exponential_backoff() {
        let policy = RetryPolicy {
            backoff: BackoffStrategy::Exponential {
                base: Duration::from_millis(100),
                multiplier: 2.0,
                max_delay: Duration::from_secs(5),
                jitter: false,
            },
            ..RetryPolicy::default()
        };
        assert_eq!(policy.delay_for_attempt(0), Duration::from_millis(100));
        assert_eq!(policy.delay_for_attempt(1), Duration::from_millis(200));
        assert_eq!(policy.delay_for_attempt(2), Duration::from_millis(400));
    }

    #[test]
    fn test_max_attempts() {
        let policy = RetryPolicy {
            max_attempts: 3,
            ..RetryPolicy::default()
        };
        assert!(policy.should_retry(0));
        assert!(policy.should_retry(2));
        assert!(!policy.should_retry(3));
    }
}
