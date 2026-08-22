RFC: RFC-0302
Title: Workflow Language
Status: Proposed
Version: 1.0.0
Author: Atlas Spe
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Workflow Language | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| DSL | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Declaration | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Expression | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Statement | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Type System | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Schema | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Template | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Variable | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Attribute | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Annotation | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Directive | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
cification Committee
Created: 2026-07-01
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
  - RFC-0004 Runtime Scheduler
  - RFC-0005 Runtime Event Bus
  - RFC-0006 Runtime State Management
  - RFC-1001 Common Event Model
  - RFC-1002 Common State Model
  - RFC-1003 Common Capability Model
  - RFC-1004 Common Contract Model
  - RFC-1005 Common Manifest Model
  - RFC-1006 Common Error Model
Supersedes: None
Superseded By: None
Category: Workflow
Layer: Standard
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0012
Constitution References:
  - Section 1 (Workflow Philosophy)
Related RFCs:
  - RFC-0303 Workflow Execution
  - RFC-0304 Workflow Runtime
  - RFC-0305 Workflow Lifecycle
  - RFC-0306 Workflow State
  - RFC-0307 Workflow Context
  - RFC-0308 Workflow Events
  - RFC-0309 Workflow Actions
  - RFC-0310 Workflow Conditions
  - RFC-0311 Workflow Triggers
  - RFC-0312 Workflow Scheduler
  - RFC-0313 Workflow Parallelism
  - RFC-0314 Workflow Error Handling
  - RFC-0315 Workflow Recovery
  - RFC-0316 Workflow Debugging
  - RFC-0317 Workflow Validation
  - RFC-0318 Workflow Versioning
  - RFC-0319 Workflow Security
  - RFC-0320 Workflow Performance
  - RFC-0321 Workflow Observability
  - RFC-0322 Workflow Extension
  - RFC-0323 Workflow Plugin Integration
  - RFC-0324 Workflow Storage
  - RFC-0325 Workflow AI
  - RFC-0326 Workflow Vision
  - RFC-0327 Workflow IPC
  - RFC-0328 Workflow Serialization
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x

Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/ast-node.json
  - schemas/workflow/variable-declaration.json
Related Catalog:
  - catalog/workflow-variable-types.md
  - catalog/workflow-node-types.md
  - catalog/workflow-manifest.md
---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.

The Workflow Language specification defines the declarative syntax, structural model, and semantic rules for expressing workflow definitions in Atlas. Workflow language definitions are abstract representations of execution graphs, not executable code. The language describes WHAT must happen through graph declarations, node definitions, edge specifications, condition expressions, and resource constraints.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0302 workflow language.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## 2 Workflow Language Philosophy

Workflow language definitions express declarative orchestration intent. They are NOT scripts. They are NOT programs. They are NOT automation macros. The workflow language defines a structured graph declaration model where:

- Nodes declare atomic units of work and their interfaces
- Edges declare data flow, control flow, and dependency relationships
- Conditions declare decision points that govern execution paths
- Resources declare constraints and requirements
- Parameters declare configurable values
- Variables declare scoped data containers

The language is implementation-independent. No concrete programming language syntax is prescribed. The grammar describes abstract constructs that any implementation MAY translate into its native representation.

---

## 3 Goals

| Goal | Description | Verification Method |
|---|---|---|
| Declarative Syntax | Workflow definitions MUST express intent, not implementation. | Syntax review |
| Graph Structure | Definitions MUST represent directed graphs. | Graph construction test |
| Type Safety | Variable and parameter types MUST be declared and enforced. | Type checking test |
| Scoping Rules | Variables MUST follow well-defined scoping rules. | Scope resolution test |
| Extensibility | New node types MUST be declarable without language changes. | Extension test |
| Package Structure | Workflow definitions MUST be packagable as complete units. | Packaging test |

---

## 4 Abstract Syntax Tree Model

### 4.1 AST Overview

Every workflow definition is represented as an Abstract Syntax Tree (AST). The AST captures the hierarchical structure of the workflow graph, including nodes, edges, conditions, parameters, and resources.

### 4.2 AST Node Types

| AST Node | Description | Children |
|---|---|---|
| Workflow | Root node representing the complete workflow | Nodes, Edges, Variables, Parameters |
| Node | Represents an atomic unit of work | Inputs, Outputs, Conditions, Actions |
| Edge | Represents a connection between nodes | Source, Target, Transformation |
| Condition | Represents a boolean expression | Left Operand, Operator, Right Operand |
| Variable | Represents a scoped data container | Type, Default Value |
| Parameter | Represents a configurable value | Type, Default Value |
| Resource | Represents a resource requirement | Type, Quantity, Constraints |
| SubGraph | Represents a nested workflow | Nodes, Edges, Variables |

### 4.3 AST Properties

- The root node MUST be a Workflow node.
- Every Workflow node MUST have at least one child Node.
- Every Node child MUST have a unique identifier.
- Every Edge child MUST reference valid source and target Node identifiers.
- Every Condition child MUST reference valid Variable or Parameter identifiers.

---

## 5 Graph Declaration Model

### 5.1 Graph Declaration

A workflow graph is declared through a set of node declarations and edge declarations. Each node declares its type, inputs, outputs, parameters, and constraints. Each edge declares its source, target, type, and optional transformation.

### 5.2 Node Declaration

Every node declaration MUST include:

- A unique identifier within the workflow graph
- A node type (from the node type catalog in RFC-0301)
- An optional human-readable label
- An optional description
- Zero or more input variable bindings
- Zero or more output variable bindings
- Zero or more configuration parameters
- Zero or more conditions that gate execution
- Zero or more actions performed during execution
- Zero or more resource requirements
- An optional execution budget
- An optional priority level
- An optional timeout duration
- An optional retry policy
- An optional error handler configuration
- An optional recovery policy

### 5.3 Edge Declaration

Every edge declaration MUST include:

- A unique identifier within the workflow graph
- A source node identifier
- A target node identifier
- An edge type (data, control, condition, event, resource, signal)

Optional edge attributes include:

- A condition that gates edge traversal
- A transformation applied to data flowing along the edge
- A cardinality (one-to-one, one-to-many, many-to-one, many-to-many)
- A timeout for data transfer
- A buffer size limit

### 5.4 Sub-Graph Declaration

Sub-graphs are declared as nested workflow definitions within a composite node. Sub-graphs inherit the parent context and may declare their own variables, parameters, and resources scoped to the sub-graph.

---

## 6 Variable Declaration and Scoping Rules

### 6.1 Variable Scope Levels

Variables in workflow definitions follow a hierarchical scoping model:

| Scope Level | Description | Lifetime |
|---|---|---|
| Workflow | Declared at the workflow root | Entire workflow execution |
| Node | Declared within a node | Node execution only |
| Sub-Graph | Declared within a sub-graph | Sub-graph execution only |
| Edge | Declared within an edge | Edge data transfer only |

### 6.2 Variable Visibility

- Variables declared at a higher scope level ARE visible at lower scope levels.
- Variables declared at a lower scope level ARE NOT visible at higher scope levels.
- Variables declared at the same scope level MUST have unique identifiers.
- Variables MAY be shadowed by variables with the same identifier in a nested scope.

### 6.3 Variable Types

Every variable MUST have a declared type. Supported variable types include:

| Type | Description | Constraints |
|---|---|---|
| String | Textual data | No length constraint |
| Integer | Whole number | Signed 64-bit |
| Float | Floating-point number | IEEE 754 double |
| Boolean | True or false | Binary |
| Array | Ordered collection | Homogeneous elements |
| Object | Key-value map | String keys |
| Null | Absence of value | Single value |
| Duration | Time interval | Positive duration |
| Timestamp | Point in time | ISO 8601 format |

---

## 7 Parameter Binding and Resolution

### 7.1 Parameter Declaration

Parameters are configurable values declared at the workflow or node level. Parameters enable workflow definitions to be reused with different configurations.

### 7.2 Parameter Binding

During execution, parameters are bound to concrete values:

- Workflow-level parameters are bound at workflow instantiation.
- Node-level parameters are bound at node initialization.
- Parameters MAY have default values.
- Parameters WITHOUT default values MUST be bound before execution.
- Parameter values MAY be overridden at execution time.

### 7.3 Parameter Resolution Order

Parameter resolution follows this order:

1. Explicit value passed at instantiation
2. Default value declared in the definition
3. Value inherited from parent context
4. Error if no value is available

---

## 8 Resource Declaration and Constraints

### 8.1 Resource Declaration

Resources are declared as requirements that must be satisfied before a node can execute. Resource declarations include:

- Resource type (CPU, memory, GPU, storage, network, custom)
- Resource quantity
- Resource constraints (minimum, maximum)
- Resource affinity (preferred location)

### 8.2 Resource Constraints

| Constraint | Description | Enforcement |
|---|---|---|
| Minimum | Minimum resource quantity required | Pre-execution check |
| Maximum | Maximum resource quantity available | Runtime enforcement |
| Affinity | Preferred resource location | Scheduler optimization |
| Exclusion | Resources that cannot coexist | Mutual exclusion check |

---

## 9 Execution Budget Declaration

### 9.1 Budget Components

Each workflow instance declares an execution budget consisting of:

| Component | Description | Unit |
|---|---|---|
| Time | Maximum execution duration | Duration |
| Nodes | Maximum node executions | Count |
| Events | Maximum event emissions | Count |
| Data Transfer | Maximum data volume | Bytes |
| Resource Units | Maximum resource consumption | Units |

### 9.2 Budget Enforcement

Budget enforcement occurs at the following points:

1. **Pre-execution**: Budget is validated against available resources.
2. **During execution**: Budget consumption is tracked per node.
3. **At completion**: Remaining budget is reported in observability data.
4. **On violation**: Budget violations cause workflow termination.

---

## 10 Priority and Scheduling Hints

### 10.1 Priority Levels

Workflow instances and individual nodes MAY declare priority levels that influence scheduling:

| Priority | Value | Description |
|---|---|---|
| Critical | 0 | Highest priority, must execute immediately |
| High | 1 | Above-normal priority |
| Normal | 2 | Default priority |
| Low | 3 | Below-normal priority |
| Background | 4 | Lowest priority, executes when resources are available |

### 10.2 Scheduling Hints

Nodes MAY provide scheduling hints to the scheduler:

- **Deadline**: Hard deadline for node completion
- **Preferred Time Window**: Time window when node execution is preferred
- **Location Preference**: Preferred execution location
- **Dependency Hint**: Hints about expected dependency satisfaction time

---

## 11 Workflow Package Structure

### 11.1 Package Layout

A workflow package is a self-contained unit that includes:

| Element | Description | Required |
|---|---|---|
| Manifest | Workflow metadata and configuration | YES |
| Definition | Workflow graph definition | YES |
| Variables | Variable type declarations | NO |
| Parameters | Parameter declarations with defaults | NO |
| Resources | Resource requirement declarations | NO |
| Templates | Reusable sub-graph templates | NO |
| Documentation | Human-readable workflow documentation | NO |

### 11.2 Manifest Integration

The workflow manifest extends the common manifest model (RFC-1005) with workflow-specific fields:

- **workflow_id**: Unique workflow identifier
- **workflow_version**: Semantic version of the workflow definition
- **entry_points**: List of entry node identifiers
- **exit_points**: List of exit node identifiers
- **node_types**: List of node types used in the workflow
- **variable_declarations**: List of variable declarations
- **parameter_declarations**: List of parameter declarations
- **resource_requirements**: List of resource requirements
- **execution_budget**: Execution budget constraints
- **priority**: Default priority level

---

## 12 Example Workflow Graphs

### 12.1 Simple Sequential Workflow

`mermaid
graph LR
    A[Entry] --> B[Node 1]
    B --> C[Node 2]
    C --> D[Node 3]
    D --> E[Exit]
`

### 12.2 Branching Workflow

`mermaid
graph TD
    A[Entry] --> B{Condition}
    B -->|True| C[Path A]
    B -->|False| D[Path B]
    C --> E[Join]
    D --> E
    E --> F[Exit]
`

### 12.3 Parallel Fan-Out Fan-In Workflow

`mermaid
graph TD
    A[Entry] --> B[Fan-Out]
    B --> C1[Worker 1]
    B --> C2[Worker 2]
    B --> C3[Worker 3]
    C1 --> D[Fan-In]
    C2 --> D
    C3 --> D
    D --> E[Exit]
`

### 12.4 Conditional Loop Workflow

`mermaid
graph TD
    A[Entry] --> B[Initialize]
    B --> C{Iteration}
    C -->|Continue| D[Process]
    C -->|Done| E[Finalize]
    D --> C
    E --> F[Exit]
`

---

## 13 Validation Rules for Language Constructs

### 13.1 Structural Validation

| Rule | Description | Severity |
|---|---|---|
| Root Node | Definition MUST have a Workflow root node | Error |
| Entry Points | Graph MUST have at least one entry node | Error |
| Exit Points | Graph SHOULD have at least one exit node | Warning |
| Unique IDs | All node and edge IDs MUST be unique | Error |
| Valid References | All edge references MUST point to existing nodes | Error |
| Acyclic Graph | Execution graph MUST be acyclic | Error |
| Connected Graph | All nodes MUST be reachable from entry | Error |

### 13.2 Semantic Validation

| Rule | Description | Severity |
|---|---|---|
| Type Consistency | Variable types MUST be consistent across edges | Error |
| Parameter Binding | All required parameters MUST be bound | Error |
| Resource Availability | Declared resources MUST be available | Warning |
| Budget Sufficiency | Execution budget MUST be sufficient | Warning |
| Condition Validity | Condition expressions MUST be well-formed | Error |

---

## 14 Acceptance Criteria

### 14.1 Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The AST model MUST support at least eight AST node types. | AST construction test |
| AC-02 | Node declarations MUST include all required attributes. | Declaration validation test |
| AC-03 | Edge declarations MUST include all required attributes. | Edge validation test |
| AC-04 | Sub-graphs MUST be declarable within composite nodes. | Sub-graph declaration test |

### 14.2 Variables

| # | Criterion | Verification Method |
|---|---|---|
| AC-05 | Four variable scope levels MUST be supported. | Scope resolution test |
| AC-06 | Nine variable types MUST be supported. | Type enumeration test |
| AC-07 | Variable shadowing MUST be supported in nested scopes. | Shadowing test |

### 14.3 Parameters

| # | Criterion | Verification Method |
|---|---|---|
| AC-08 | Four-parameter resolution order levels MUST be defined. | Resolution order test |
| AC-09 | Default parameter values MUST be supported. | Default value test |

### 14.4 Resources

| # | Criterion | Verification Method |
|---|---|---|
| AC-10 | Four resource constraint types MUST be supported. | Constraint test |

### 14.5 Budget

| # | Criterion | Verification Method |
|---|---|---|
| AC-11 | Five budget components MUST be definable. | Budget declaration test |

### 14.6 Validation

| # | Criterion | Verification Method |
|---|---|---|
| AC-12 | Seven structural validation rules MUST be enforced. | Validation test suite |
| AC-13 | Five semantic validation rules MUST be enforced. | Validation test suite |

---

## 15 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview |
| RFC-0303 | Workflow Execution |
| RFC-0306 | Workflow State |
| RFC-0307 | Workflow Context |
| RFC-0309 | Workflow Actions |
| RFC-0310 | Workflow Conditions |
| RFC-0312 | Workflow Scheduler |
| RFC-0320 | Workflow Performance |
| RFC-1005 | Common Manifest Model |
| Glossary | Atlas Master Glossary |

---

## 14 Terminology

| Term | Definition | Source |
|---|---|---|
| Workflow Definition | A declarative graph specification expressing WHAT must happen, not HOW. | RFC-0301 |
| Abstract Syntax Tree | The hierarchical representation of a workflow definition structure. | This RFC |
| Node Declaration | A specification of an atomic unit of work within a workflow graph. | This RFC |
| Edge Declaration | A specification of a connection between nodes representing data or control flow. | This RFC |
| Variable Scope | The visibility domain of a variable within the workflow definition hierarchy. | This RFC |
| Parameter Resolution | The ordered process of determining parameter values from available sources. | This RFC |
| Template | A reusable sub-graph definition that can be instantiated within a workflow. | This RFC |

## 15 Layer Boundaries

### 15.1 Responsibilities
This specification IS responsible for: defining the workflow language grammar, specifying the AST model, defining variable and parameter scoping rules, and establishing the package structure for workflow definitions.

### 15.2 Non-Responsibilities
This specification IS NOT responsible for: executing workflow definitions (delegated to RFC-0303), validating workflow definitions (delegated to RFC-0317), or serializing workflow definitions (delegated to RFC-0328).

### 15.3 Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |
| RFC-0303 | Consumed | Workflow Execution consumes language definitions |
| RFC-0306 | Consumed | Workflow State uses language-defined state |
| RFC-0307 | Consumed | Workflow Context uses language variables |
| RFC-0309 | Consumed | Workflow Actions uses language node declarations |
| RFC-0310 | Consumed | Workflow Conditions uses language condition expressions |
| RFC-0317 | Consumed | Workflow Validation validates language constructs |
| RFC-0328 | Consumed | Workflow Serialization serializes language definitions |

### 15.4 Consumers
- Workflow Execution (RFC-0303): Consumes language definitions for execution.
- Workflow State (RFC-0306): Uses language-defined state model.
- Workflow Context (RFC-0307): Uses language variable declarations.
- Workflow Actions (RFC-0309): Uses language node declarations.

### 15.5 Providers
- AST Node Schema (schemas/workflow/ast-node.json): Provides the AST format contract.
- Variable Declaration Schema (schemas/workflow/variable-declaration.json): Provides the variable format contract.
- Variable Types Catalog (catalog/workflow-variable-types.md): Provides the variable type taxonomy.
- Node Types Catalog (catalog/workflow-node-types.md): Provides the node type taxonomy.

### 15.6 Forbidden Dependencies
- This specification MUST NOT prescribe any concrete programming language syntax.
- This specification MUST NOT depend on any specific file format (YAML, JSON, TOML).

## 16 Future Evolution
- **Domain-Specific Workflow Languages**: Specialized languages for specific workflow domains.
- **Visual Workflow Editors**: Graphical workflow definition tools with language-level guarantees.
- **Workflow Language Interop**: Translation between different workflow language representations.
- **Typed Workflow Definitions**: Strong typing with compile-time type checking.

## 17 Runtime Independence
This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:
- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)

## 18 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0303 | Workflow Execution (language consumption) |
| RFC-0306 | Workflow State (language-defined state) |
| RFC-0307 | Workflow Context (language variables) |
| RFC-0309 | Workflow Actions (language node declarations) |
| RFC-0310 | Workflow Conditions (language conditions) |
| RFC-0312 | Workflow Scheduler (language scheduling) |
| RFC-0317 | Workflow Validation (language validation) |
| RFC-0320 | Workflow Performance (language performance) |
| RFC-0328 | Workflow Serialization (language serialization) |
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/ast-node.json | AST Node JSON Schema |
| schemas/workflow/variable-declaration.json | Variable Declaration JSON Schema |
| catalog/workflow-variable-types.md | Variable Types Catalog |
| catalog/workflow-node-types.md | Node Types Catalog |
| catalog/workflow-manifest.md | Manifest Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0302 (this document), RFC-0301 (Overview), RFC-0303 (Execution) |
---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |
| 1.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Enterprise specification upgrade: added Authority, Terminology, Layer Boundaries, Runtime Independence, Future Evolution, Compliance Matrix, and verifiable Acceptance Criteria |


## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | N/A |
| Related Catalog | N/A |
