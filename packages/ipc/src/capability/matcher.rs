//! Capability matcher - matches capabilities between endpoints.

use super::version::{Version, VersionMatcher};
use super::resolver::Capability;

/// Matches capabilities between two endpoints.
pub struct CapabilityMatcher;

impl CapabilityMatcher {
    pub fn match_capabilities(
        local: &Capability,
        remote: &Capability,
    ) -> bool {
        if local.name != remote.name {
            return false;
        }
        let local_ver = Version::parse(&local.version);
        let remote_ver = Version::parse(&remote.version);
        match (local_ver, remote_ver) {
            (Some(lv), Some(rv)) => VersionMatcher::are_compatible(&lv, &rv),
            _ => true,
        }
    }

    pub fn find_matches<'a>(
        local_caps: &'a [Capability],
        remote_caps: &'a [Capability],
    ) -> Vec<(&'a Capability, &'a Capability)> {
        let mut matches = Vec::new();
        for local in local_caps {
            for remote in remote_caps {
                if Self::match_capabilities(local, remote) {
                    matches.push((local, remote));
                }
            }
        }
        matches
    }

    pub fn all_required_match(
        local_caps: &[Capability],
        remote_caps: &[Capability],
    ) -> bool {
        for local in local_caps.iter().filter(|c| c.required) {
            let found = remote_caps.iter().any(|remote| {
                Self::match_capabilities(local, remote)
            });
            if !found {
                return false;
            }
        }
        true
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_match_capabilities() {
        let local = Capability::required("auth", "1.0.0");
        let remote = Capability::required("auth", "1.5.0");
        assert!(CapabilityMatcher::match_capabilities(&local, &remote));
    }

    #[test]
    fn test_mismatched_names() {
        let local = Capability::required("auth", "1.0.0");
        let remote = Capability::required("compute", "1.0.0");
        assert!(!CapabilityMatcher::match_capabilities(&local, &remote));
    }

    #[test]
    fn test_major_version_mismatch() {
        let local = Capability::required("auth", "1.0.0");
        let remote = Capability::required("auth", "2.0.0");
        assert!(!CapabilityMatcher::match_capabilities(&local, &remote));
    }
}
