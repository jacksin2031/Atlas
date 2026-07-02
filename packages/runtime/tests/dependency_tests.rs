//! Dependency resolver tests.

use atlas_runtime::dependency::DependencyResolver;
use atlas_runtime::registry::ServiceRegistry;
use atlas_common::{ServiceDeclaration, DependencyError};

#[test]
fn test_empty_dependency_resolution() {
    let resolver = DependencyResolver::new();
    let reg = ServiceRegistry::new();
    let order = resolver.resolve(&reg).unwrap();
    assert!(order.is_empty());
}

#[test]
fn test_single_service_resolution() {
    let resolver = DependencyResolver::new();
    let mut reg = ServiceRegistry::new();
    reg.register_declaration(ServiceDeclaration {
        id: "svc-1".to_string(), name: "S1".to_string(), version: "1.0".to_string(),
        dependencies: vec![], required: true, priority: 0,
    }).unwrap();
    let order = resolver.resolve(&reg).unwrap();
    assert_eq!(order.len(), 1);
    assert_eq!(order[0], "svc-1");
}

#[test]
fn test_linear_dependency_chain() {
    let resolver = DependencyResolver::new();
    let mut reg = ServiceRegistry::new();
    // C has no deps, B depends on C, A depends on B
    reg.register_declaration(ServiceDeclaration {
        id: "c".to_string(), name: "C".to_string(), version: "1.0".to_string(),
        dependencies: vec![], required: true, priority: 0,
    }).unwrap();
    reg.register_declaration(ServiceDeclaration {
        id: "b".to_string(), name: "B".to_string(), version: "1.0".to_string(),
        dependencies: vec!["c".to_string()], required: true, priority: 1,
    }).unwrap();
    reg.register_declaration(ServiceDeclaration {
        id: "a".to_string(), name: "A".to_string(), version: "1.0".to_string(),
        dependencies: vec!["b".to_string()], required: true, priority: 2,
    }).unwrap();

    let order = resolver.resolve(&reg).unwrap();
    assert_eq!(order.len(), 3);
    // C should come before B, B before A
    assert!(order.iter().position(|x| x == "c").unwrap() < order.iter().position(|x| x == "b").unwrap());
    assert!(order.iter().position(|x| x == "b").unwrap() < order.iter().position(|x| x == "a").unwrap());
}

#[test]
fn test_cycle_detection() {
    let resolver = DependencyResolver::new();
    let mut reg = ServiceRegistry::new();
    // A depends on B, B depends on A = cycle
    reg.register_declaration(ServiceDeclaration {
        id: "a".to_string(), name: "A".to_string(), version: "1.0".to_string(),
        dependencies: vec!["b".to_string()], required: true, priority: 0,
    }).unwrap();
    reg.register_declaration(ServiceDeclaration {
        id: "b".to_string(), name: "B".to_string(), version: "1.0".to_string(),
        dependencies: vec!["a".to_string()], required: true, priority: 1,
    }).unwrap();

    let result = resolver.resolve(&reg);
    assert!(result.is_err());
    assert!(matches!(result.unwrap_err(), DependencyError::CircularDependency(_)));
}
