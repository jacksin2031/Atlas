//! Service Registry tests.

use atlas_runtime::registry::ServiceRegistry;
use atlas_common::{ServiceDeclaration, ServiceError};

#[test]
fn test_empty_registry() {
    let reg = ServiceRegistry::new();
    assert!(reg.is_empty());
    assert_eq!(reg.len(), 0);
}

#[test]
fn test_register_service() {
    let mut reg = ServiceRegistry::new();
    let decl = ServiceDeclaration {
        id: "svc-1".to_string(),
        name: "Test Service".to_string(),
        version: "1.0.0".to_string(),
        dependencies: vec![],
        required: true,
        priority: 0,
    };
    reg.register_declaration(decl).unwrap();
    assert_eq!(reg.len(), 1);
    assert!(!reg.is_empty());
}

#[test]
fn test_duplicate_registration() {
    let mut reg = ServiceRegistry::new();
    let decl = ServiceDeclaration {
        id: "svc-1".to_string(),
        name: "Test".to_string(),
        version: "1.0.0".to_string(),
        dependencies: vec![],
        required: true,
        priority: 0,
    };
    reg.register_declaration(decl.clone()).unwrap();
    let result = reg.register_declaration(decl);
    assert!(result.is_err());
    assert_eq!(result.unwrap_err(), ServiceError::DuplicateRegistration("svc-1".to_string()));
}

#[test]
fn test_lookup_success() {
    let mut reg = ServiceRegistry::new();
    reg.register_declaration(ServiceDeclaration {
        id: "svc-2".to_string(),
        name: "Lookup Test".to_string(),
        version: "1.0.0".to_string(),
        dependencies: vec!["svc-1".to_string()],
        required: true,
        priority: 1,
    }).unwrap();
    assert_eq!(reg.len(), 1);
}

#[test]
fn test_lookup_not_found() {
    let reg = ServiceRegistry::new();
    let result = reg.get("nonexistent");
    assert!(result.is_err());
}

#[test]
fn test_service_ids() {
    let mut reg = ServiceRegistry::new();
    reg.register_declaration(ServiceDeclaration {
        id: "a".to_string(), name: "A".to_string(), version: "1.0".to_string(),
        dependencies: vec![], required: true, priority: 0,
    }).unwrap();
    reg.register_declaration(ServiceDeclaration {
        id: "b".to_string(), name: "B".to_string(), version: "1.0".to_string(),
        dependencies: vec!["a".to_string()], required: true, priority: 1,
    }).unwrap();

    let ids = reg.service_ids();
    assert_eq!(ids.len(), 2);
}

#[test]
fn test_deinitialize_all_returns_reverse() {
    let mut reg = ServiceRegistry::new();
    reg.register_declaration(ServiceDeclaration {
        id: "first".to_string(), name: "First".to_string(), version: "1.0".to_string(),
        dependencies: vec![], required: true, priority: 0,
    }).unwrap();
    reg.register_declaration(ServiceDeclaration {
        id: "second".to_string(), name: "Second".to_string(), version: "1.0".to_string(),
        dependencies: vec!["first".to_string()], required: true, priority: 1,
    }).unwrap();

    let reversed = reg.deinitialize_all().unwrap();
    assert_eq!(reversed.len(), 2);
    // Reverse order: second, first
    assert_eq!(reversed[0], "second");
    assert_eq!(reversed[1], "first");
}
