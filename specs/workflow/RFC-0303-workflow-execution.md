RFC: RFC-0303
Title: Workflow Execution
Status: Proposed
Version: 1.0.0
Author: Atlas 
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Execution Engine | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Execution Context | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Execution Stack | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Frame | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Tick | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Result | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Output | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Side Effect | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Execution Plan | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Execution Order | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
Specification Committee
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
Layer: Core
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0012
Constitution References:
  - Section 1 (Workflow Philosophy)
Related RFCs:
  - RFC-0301 Workflow Overview
  - RFC-0302 Workflow Language
  - RFC-0304 Workflow Runtime
  - RFC-0305 Workflow Lifecycle
  - RFC-0306 Workflow State
  - RFC-0307 Workflow Context
  - RFC-0308 Workflow Events
  - RFC-0309 Workflow Actions
  - RFC-0310 Workflow Conditions
  - RFC-0313 Workflow Parallelism
  - RFC-0314 Workflow Error Handling
  - RFC-0317 Workflow Validation
  - RFC-0320 Workflow Performance
  - RFC-0321 Workflow Observability
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/execution-state.json
  - schemas/workflow/result-propagation.json
Related Catalog:
Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/execution-state.json
  -   - schemas/workflow/result-propagation.json
Related Catalog:
  - catalog/workflow-result-types.md
  -   - catalog/workflow-status.md
  -   - catalog/workflow-actions.md

  - catalog/workflow-result-types.md
  - catalog/workflow-status.md
  - catalog/workflow-actions.md

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the execution model defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0303 workflow execution.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## Table of Contents
1. [Introduction](#1-introduction)
2. [Execution Philosophy](#2-execution-philosophy)
3. [Goals](#3-goals)
4. [Non-Goals](#4-non-goals)
5. [Execution Graph Model](#5-execution-graph-model)
6. [Execution Phases](#6-execution-phases)
7. [Node Execution Semantics](#7-node-execution-semantics)
8. [Edge Traversal and Dependency Resolution](#8-edge-traversal-and-dependency-resolution)
9. [Deterministic Execution Guarantees](#9-deterministic-execution-guarantees)
10. [Topological Sort and Execution Ordering](#10-topological-sort-and-execution-ordering)
11. [Execution Context Initialization](#11-execution-context-initialization)
12. [Result Propagation](#12-result-propagation)
13. [Execution Budget Enforcement](#13-execution-budget-enforcement)
14. [Execution Priority](#14-execution-priority)
15. [Resource Allocation During Execution](#15-resource-allocation-during-execution)
16. [Execution Fault Tolerance](#16-execution-fault-tolerance)
17. [Observability During Execution](#17-observability-during-execution)
18. [Concurrency and Parallelism in Execution](#18-concurrency-and-parallelism-in-execution)
19. [Execution Verification](#19-execution-verification)
20. [Acceptance Criteria](#20-acceptance-criteria)
21. [References](#21-references)
22. [Changelog](#22-changelog)
23. [Compatibility](#23-compatibility)

---

## 1 Introduction

The Workflow Execution specification defines how Atlas evaluates, traverses, and completes workflow graphs during runtime. Execution is the process by which a parsed and validated workflow definition becomes a sequence of observable, stateful, and recoverable node activations within the Atlas runtime.

Workflow execution is NOT imperative programming. Execution does not evaluate arbitrary code. Execution follows a declarative graph model where the structure of the workflow definition fully determines the set of possible execution paths. The execution engine selects among these paths based on conditions, dependencies, and resource availability.

The execution model is built upon the following abstractions:

- **Execution Graph**: A directed acyclic graph (DAG) derived from the workflow definition, where nodes represent atomic units of work and edges represent data flow and dependency relationships.
- **Execution Phase**: A discrete stage in the lifecycle of execution, from parsing through completion. Each phase has well-defined entry and exit conditions.
- **Node Activation**: The process of preparing, running, and concluding an individual node within the execution graph.
- **Result Propagation**: The mechanism by which outputs from one node become inputs to downstream nodes.

Execution operates within the runtime framework defined by RFC-0001 through RFC-0014 and leverages the common models defined by RFC-1001 through RFC-1006. The execution engine interacts with the runtime scheduler (RFC-0004), event bus (RFC-0005), and state manager (RFC-0006) to accomplish its duties.
---

## 2 Execution Philosophy

The execution philosophy rests upon four foundational principles:

### Principle 1: Determinism Over Flexibility

Execution MUST produce deterministic results for a given workflow definition, context, and input. Non-determinism is only permitted in explicitly defined parallel execution windows where all possible interleavings yield equivalent final states. The execution engine MUST document every non-deterministic decision point and its resolution mechanism.

### Principle 2: Graph-Structured Over Sequential

Execution follows the graph topology. Sequential execution is a special case of graph execution where the graph is a single path. The engine MUST respect all graph relationships including fan-out, fan-in, branching, and conditional paths.

### Principle 3: Observable Over Implicit

Every execution step MUST produce observable state changes and events. No execution action is invisible to the observability layer. The execution engine MUST emit events at every phase transition, node activation, and result propagation.

### Principle 4: Recoverable Over Ephemeral

Execution state MUST be persisted at defined checkpoint boundaries. The engine MUST enable recovery from any checkpoint without loss of completed work. Partial execution results MUST be preservable and resumable.

---

## 3 Goals

| Goal | Description | Verification Method |
|---|---|---|
| Graph Evaluation | Execution MUST evaluate the workflow graph deterministically. | Graph evaluation test |
| Phase Discipline | Execution MUST proceed through six defined phases. | Phase transition test |
| Node Semantics | Each node type MUST have well-defined execution semantics. | Semantics test |
| Edge Traversal | Edge traversal MUST respect dependency and data flow contracts. | Traversal test |
| Determinism | Identical inputs MUST produce identical execution traces. | Determinism test |
| Budget Enforcement | Execution MUST enforce declared budgets. | Budget test |
| Priority Handling | Execution MUST honor priority levels. | Priority test |
| Result Propagation | Results MUST propagate correctly through the graph. | Propagation test |
| Fault Tolerance | Execution MUST handle transient failures gracefully. | Fault injection test |
| Observability | Every execution step MUST be observable. | Observability test |

---

## 4 Non-Goals

The following are explicitly OUT of scope for this specification:

- **Scripting**: Execution does not support arbitrary script evaluation.
- **General-Purpose Computing**: The execution engine is not a general-purpose compute platform.
- **Data Processing Pipelines**: While workflows may process data, the execution engine itself is not a data processing framework.
- **Transaction Processing**: Execution does not provide ACID transaction semantics beyond the workflow state model.
- **Real-Time Execution**: The execution engine does not guarantee real-time execution bounds.
- **Distributed Execution**: This specification defines execution semantics; distributed deployment is covered by RFC-0327.
---

## 5 Execution Graph Model

### 5.1 Graph Construction

The execution graph is constructed from the validated workflow definition during the Plan phase. The graph is a directed acyclic graph (DAG) where:

- Each vertex represents a node from the workflow definition.
- Each edge represents a dependency or data flow relationship.
- Entry nodes have no incoming edges from other workflow nodes.
- Exit nodes have no outgoing edges to other workflow nodes.

The execution graph MUST satisfy the following invariants:

| Invariant | Description | Enforcement Point |
|---|---|---|
| Acyclicity | The graph MUST NOT contain cycles. | Validation phase |
| Connectivity | All nodes MUST be reachable from at least one entry node. | Validation phase |
| Reachability | All nodes MUST be able to reach at least one exit node. | Validation phase |
| Type Consistency | Edge data types MUST be compatible between connected nodes. | Validation phase |
| Uniqueness | Each node MUST have a unique identifier within the graph. | Definition phase |

### 5.2 Graph Representation

The execution graph is represented as an abstract structure comprising:

- **Vertices**: Node instances with their current execution state, input bindings, and output bindings.
- **Edges**: Dependency and data flow connections with their own state and transformation rules.
- **Metadata**: Graph-level metadata including the workflow definition reference, execution context reference, and phase state.

### 5.3 Execution Graph Diagram

mermaid
graph TD
    subgraph ExecutionGraph["Execution Graph"]
        E1[Entry Node] --> N1[Node Alpha]
        E1 --> N2[Node Beta]
        N1 --> N3[Node Gamma]
        N2 --> N3
        N1 --> N4[Node Delta]
        N2 --> N5[Node Epsilon]
        N3 --> X1[Exit Node]
        N4 --> X1
        N5 --> X1
    end
    
    classDef entry fill:#4CAF50,stroke:#388E3C,color:#fff
    classDef node fill:#2196F3,stroke:#1565C0,color:#fff
    classDef exit fill:#FF5722,stroke:#E64A19,color:#fff
    class E1 entry
    class N1,N2,N3,N4,N5 node
    class X1 exit


### 5.4 Graph Properties

| Property | Constraint | Rationale |
|---|---|---|
| Maximum nodes | Unlimited | Scalability requirement |
| Maximum edges per node | 100 | Prevents fan-out explosion |
| Maximum depth | 1000 | Prevents stack overflow |
| Maximum breadth | 10000 | Prevents resource exhaustion |
| Minimum nodes | 1 (entry) | A workflow MUST have at least one node |
| Minimum edges | 0 | A single-node workflow has no edges |
---

## 6 Execution Phases

Execution proceeds through six distinct phases. Each phase has well-defined entry conditions, duties, and exit conditions. No phase MAY be skipped, and phases MUST proceed in the specified order.

### 6.1 Phase Overview

| Phase | Description | Input | Output |
|---|---|---|---|
| Parse | Parse the workflow definition into an execution graph. | Workflow manifest | Execution graph AST |
| Validate | Verify the execution graph satisfies all invariants. | Execution graph AST | Validated execution graph |
| Plan | Compute execution ordering and allocate resources. | Validated execution graph | Execution plan |
| Execute | Activate nodes and traverse the graph. | Execution plan | Execution results |
| Complete | Aggregate results and finalize execution. | Execution results | Final workflow state |
| Terminate | Clean up resources and emit final events. | Final workflow state | Terminated instance |

### 6.2 Parse Phase

The Parse phase transforms the workflow definition into an executable graph representation.

**Requirements:**

1. The engine MUST parse the workflow manifest and extract all node and edge declarations.
2. The engine MUST resolve all node type references to their registered capability definitions.
3. The engine MUST construct the initial execution graph AST with all declared nodes and edges.
4. The engine MUST bind all parameter values to their corresponding declarations.
5. The engine MUST resolve all variable declarations and initialize them to their default values.

**Parse Phase State Machine:**

mermaid
stateDiagram-v2
    [*] --> Unparsed
    Unparsed --> Parsing: Manifest received
    Parsing --> Parsed: All nodes resolved
    Parsing --> ParseError: Resolution failure
    ParseError --> Unparsed: Retry
    Parsed --> [*]: Proceed to Validate


**Parse Phase Output:**

| Output | Description | Required |
|---|---|---|
| Node Registry | Map of node IDs to node definitions | YES |
| Edge Registry | Map of edge IDs to edge definitions | YES |
| Parameter Bindings | Map of parameter names to bound values | YES |
| Variable Initializations | Map of variable names to initial values | YES |
| Type Resolution Map | Map of node type references to capability definitions | YES |

### 6.3 Validate Phase

The Validate phase verifies that the execution graph satisfies all structural and semantic invariants.

**Requirements:**

1. The engine MUST verify that the graph is acyclic.
2. The engine MUST verify that all nodes are reachable from at least one entry node.
3. The engine MUST verify that all nodes can reach at least one exit node.
4. The engine MUST verify that all edge data types are compatible.
5. The engine MUST verify that all required parameters are bound.
6. The engine MUST verify that all referenced capabilities are available.
7. The engine MUST verify that declared resource requirements can be satisfied.

**Validation Rules:**

| Rule ID | Rule | Severity | Description |
|---|---|---|---|
| V-001 | Acyclicity | Error | Graph MUST NOT contain cycles |
| V-002 | Entry Reachability | Error | All nodes MUST be reachable from entry |
| V-003 | Exit Reachability | Error | All nodes MUST be able to reach exit |
| V-004 | Type Compatibility | Error | Edge data types MUST be compatible |
| V-005 | Parameter Binding | Error | All required parameters MUST be bound |
| V-006 | Capability Availability | Error | Referenced capabilities MUST be available |
| V-007 | Resource Sufficiency | Warning | Declared resources SHOULD be available |
| V-008 | Budget Sufficiency | Warning | Execution budget SHOULD be sufficient |
| V-009 | Condition Validity | Error | Condition expressions MUST be well-formed |
| V-010 | Unique IDs | Error | All node and edge IDs MUST be unique |
| V-011 | Self-Reference | Error | Nodes MUST NOT reference themselves |
| V-012 | Orphan Nodes | Error | Nodes MUST have at least one connection |

### 6.4 Plan Phase

The Plan phase computes the execution ordering and allocates resources for the upcoming execution.

**Requirements:**

1. The engine MUST compute a topological ordering of all nodes.
2. The engine MUST identify parallel execution groups (nodes that can execute concurrently).
3. The engine MUST allocate resources based on declared requirements.
4. The engine MUST establish execution budgets and timeouts.
5. The engine MUST register all event handlers for the execution.

**Planning Output:**

| Output | Description |
|---|---|
| Execution Order | Total order of node activations respecting dependencies |
| Parallel Groups | Sets of nodes eligible for concurrent execution |
| Resource Allocation | Mapping of nodes to allocated resources |
| Budget Assignments | Per-node and per-group budget allocations |
| Event Handler Registration | List of registered event handlers |

### 6.5 Execute Phase

The Execute phase activates nodes and traverses the execution graph according to the execution plan.

**Requirements:**

1. The engine MUST activate nodes in accordance with the execution plan.
2. The engine MUST respect dependency relationships when activating nodes.
3. The engine MUST propagate results from completed nodes to dependent nodes.
4. The engine MUST evaluate conditions at conditional edges before traversal.
5. The engine MUST enforce execution budgets for each node and the overall graph.
6. The engine MUST emit events for every node activation and completion.
7. The engine MUST persist checkpoints at defined boundaries.

### 6.6 Complete Phase

The Complete phase aggregates results, finalizes the execution state, and prepares for termination.

**Requirements:**

1. The engine MUST aggregate all node results into the final output.
2. The engine MUST verify that all exit conditions are satisfied.
3. The engine MUST compute the final workflow state.
4. The engine MUST persist the final state checkpoint.
5. The engine MUST emit completion or failure events.

### 6.7 Terminate Phase

The Terminate phase performs cleanup and releases all resources.

**Requirements:**

1. The engine MUST release all allocated resources.
2. The engine MUST flush all observability data.
3. The engine MUST emit the final termination event.
4. The engine MUST update the workflow instance state to terminated.
5. The engine MUST clean up all execution context artifacts.
---

## 7 Node Execution Semantics

### 7.1 Node Activation

Each node activation follows a defined sequence:

mermaid
sequenceDiagram
    participant Scheduler
    participant Engine
    participant Node
    participant EventBus
    participant StateManager
    
    Scheduler->>Engine: Schedule node activation
    Engine->>Node: Prepare inputs from context
    Node->>Node: Evaluate preconditions
    alt Preconditions met
        Node->>Node: Execute node logic
        Node->>Engine: Return result
        Engine->>Engine: Capture result
        Engine->>EventManager: Persist node state
        Engine->>EventBus: Emit NodeStarted
        Engine->>EventBus: Emit NodeCompleted
    else Preconditions not met
        Node->>Engine: Return precondition failure
        Engine->>EventManager: Record failure state
        Engine->>EventBus: Emit NodeFailed
    end
    Engine->>Scheduler: Report activation complete


### 7.2 Node Activation Sequence

| Step | Action | Description |
|---|---|---|
| 1 | Input Preparation | Gather all inputs from upstream node results and context variables. |
| 2 | Precondition Evaluation | Evaluate all preconditions declared by the node. |
| 3 | Resource Acquisition | Acquire all resources declared by the node. |
| 4 | Execution | Perform the node's declared work. |
| 5 | Result Capture | Capture and validate the node's outputs. |
| 6 | State Persistence | Persist the node's execution state. |
| 7 | Event Emission | Emit completion or failure events. |
| 8 | Resource Release | Release acquired resources. |

### 7.3 Node Execution States

During execution, each node transitions through the following states:

| State | Description | Entry Condition | Exit Condition |
|---|---|---|---|
| Pending | Node is waiting for dependencies. | All upstream nodes not completed. | All dependencies satisfied. |
| Ready | Node is scheduled for activation. | Dependencies satisfied, resources available. | Activation begins. |
| Running | Node is actively executing. | Activation succeeds. | Execution completes or fails. |
| Waiting | Node is blocked on external condition. | External condition not met. | Condition is met. |
| Completed | Node execution succeeded. | Execution produces valid output. | Results propagated. |
| Failed | Node execution failed. | Execution produces error. | Error handled or propagated. |
| Cancelled | Node execution was cancelled. | Cancellation request received. | Cleanup complete. |
| Compensated | Node's compensation executed. | Compensation required. | Compensation complete. |

### 7.4 Node Type Execution Semantics

Different node types have specific execution semantics:

| Node Type | Execution Behavior | Special Rules |
|---|---|---|
| Leaf | Executes atomic work unit. | No upstream dependencies. |
| Intermediate | Processes inputs and produces outputs. | All inputs MUST be available. |
| Branch | Evaluates condition and selects path. | Exactly one outgoing path activated. |
| Merge | Waits for all incoming paths. | All inputs MUST arrive. |
| Fan-Out | Distributes work to parallel paths. | All outputs collected at merge. |
| Fan-In | Collects results from parallel paths. | Waits for all inputs. |
| Loop | Repeats execution until condition. | Iteration count bounded by budget. |
| Wait | Suspends until signal or timeout. | Timeout enforced by budget. |
| Signal | Sends notification to downstream. | Signal propagates to all listeners. |
| Compensate | Reverses prior work. | Compensation order is reverse-execution. |

### 7.5 Node Execution Contract

Every node execution MUST satisfy the following contract:

| Contract Element | Requirement | Enforcement |
|---|---|---|
| Input Completeness | All declared inputs MUST be present. | Pre-execution check |
| Type Safety | Input types MUST match declared types. | Type checker |
| Budget Compliance | Execution MUST NOT exceed budget. | Runtime monitor |
| State Transition | Node state MUST advance monotonically. | State machine |
| Event Emission | Appropriate events MUST be emitted. | Event bus |
| Result Validity | Outputs MUST conform to declared schema. | Post-execution check |
| Cleanup | Resources MUST be released. | Post-execution hook |
---

## 8 Edge Traversal and Dependency Resolution

### 8.1 Edge Types

Edges in the execution graph represent different kinds of relationships:

| Edge Type | Purpose | Traversal Rule |
|---|---|---|
| Data Flow | Carries output data between nodes. | Traversed when source completes. |
| Control Flow | Governs execution ordering. | Traversed when source completes. |
| Dependency | Declares prerequisite relationship. | Source MUST complete before target. |
| Conditional | Activated only when condition is true. | Condition MUST evaluate to true. |
| Exception | Routes to error handler. | Activated when source fails. |
| Compensation | Routes to compensation action. | Activated during rollback. |

### 8.2 Edge State

Each edge transitions through the following states during execution:

| State | Description |
|---|---|
| Inactive | Edge is not yet eligible for traversal. |
| Eligible | Source node has completed; edge may be traversed. |
| Active | Edge is being traversed; data is flowing. |
| Consumed | Target node has received data from this edge. |
| Skipped | Edge was not traversed due to condition evaluation. |
| Broken | Edge traversal failed; error propagated. |

### 8.3 Dependency Resolution

The engine MUST resolve dependencies using the following algorithm:

1. Identify all nodes with unmet dependencies.
2. For each node, check if all predecessor nodes have reached a terminal state (Completed, Failed, or Cancelled).
3. If all predecessors are in a terminal state, mark the node as Ready.
4. If any predecessor is in a non-terminal state, the node remains Pending.
5. When a node reaches Ready state, schedule it for activation.

**Dependency Resolution Table:**

| Predecessor State | Successor State | Action |
|---|---|---|
| Completed | Ready | Schedule successor for activation. |
| Failed | Blocked | Evaluate error handling policy. |
| Cancelled | Skipped | Skip successor if not required. |
| Running | Pending | Wait for predecessor completion. |
| Waiting | Pending | Wait for predecessor completion. |

### 8.4 Edge Traversal Sequence

The edge traversal sequence follows this order:

1. Source node completes execution.
2. Source node emits completion event to the engine.
3. Engine marks all outgoing edges as Eligible.
4. For conditional edges, the engine evaluates the condition expression.
5. If the condition is true, the edge is traversed; otherwise, it is marked Skipped.
6. For unconditional edges, the edge is traversed immediately.
7. Data flows from the source edge to the target node inputs.
8. Target node acknowledges receipt.
9. Edge state transitions to Consumed.
### 8.5 Conditional Edge State Machine

mermaid
stateDiagram-v2
    [*] --> Inactive
    Inactive --> Eligible: Source completes
    Eligible --> Active: Condition is true
    Eligible --> Skipped: Condition is false
    Active --> Consumed: Data delivered
    Skipped --> [*]: Edge resolved
    Consumed --> [*]: Edge resolved


---

## 9 Deterministic Execution Guarantees

### 9.1 Determinism Requirements

The execution engine MUST guarantee deterministic execution under the following conditions:

1. **Same Definition, Same Context**: Given the same workflow definition and execution context, the engine MUST produce the same execution trace.
2. **Same Inputs, Same Outputs**: Given the same node inputs, the engine MUST produce the same node outputs.
3. **Same Conditions, Same Paths**: Given the same condition evaluations, the engine MUST traverse the same execution paths.

### 9.2 Sources of Non-Determinism

The following are the only permitted sources of non-determinism:

| Source | Mitigation |
|---|---|
| Parallel execution ordering | All interleavings MUST yield equivalent final states. |
| External time sources | Time-based conditions MUST use wall-clock time consistently. |
| Randomness | Random seeds MUST be deterministic per execution instance. |
| External service responses | Responses MUST be cached and replayed for recovery. |

### 9.3 Determinism Verification

The engine MUST support determinism verification through:

1. **Execution Trace Recording**: Every execution step MUST be recorded in a deterministic trace format.
2. **Trace Comparison**: Given two execution traces, the engine MUST be able to verify their equivalence.
3. **Replay**: Given a recorded trace, the engine MUST be able to replay the execution identically.

### 9.4 Determinism Guarantees Summary

| Guarantee | Description | Enforcement |
|---|---|---|
| Trace Determinism | Execution traces are reproducible. | Trace recorder |
| State Determinism | Final states are reproducible. | State verifier |
| Output Determinism | Node outputs are reproducible. | Output comparator |
| Path Determinism | Execution paths are reproducible. | Path comparator |
---

## 10 Topological Sort and Execution Ordering

### 10.1 Topological Sort Algorithm

The execution engine MUST compute a topological ordering of the execution graph during the Plan phase. The ordering MUST satisfy the following properties:

1. If node A is a predecessor of node B, then A appears before B in the ordering.
2. The ordering MUST be stable: given equal priority, nodes are ordered by their declaration order.
3. The ordering MUST be unique: for a given graph and priority assignment, the ordering is deterministic.

### 10.2 Execution Ordering Rules

| Rule | Description |
|---|---|
| Dependency Rule | A node MUST NOT execute before all its predecessors complete. |
| Priority Rule | Among ready nodes, higher priority nodes execute first. |
| Stability Rule | Among ready nodes with equal priority, declaration order is used. |
| Budget Rule | Node execution MUST NOT exceed its allocated budget. |
| Resource Rule | Node execution MUST NOT exceed available resources. |

### 10.3 Parallel Execution Groups

The engine MUST identify parallel execution groups during planning. A parallel execution group is a set of nodes that have no interdependencies among themselves and can therefore execute concurrently.

**Parallel Group Rules:**

| Rule | Description |
|---|---|
| Independence | Nodes within a group MUST have no interdependencies. |
| Simultaneity | All nodes in a group SHOULD execute simultaneously. |
| Atomicity | Either all nodes in a group complete, or the group is treated as failed. |
| Resource Isolation | Resources allocated to one group MUST NOT be shared with another. |

### 10.4 Parallel Group Diagram

mermaid
graph TD
    G1[Group 1: Single Node] --> G2[Group 2: Parallel Nodes A, B, C]
    G2 --> G3[Group 3: Single Node]
    G3 --> G4[Group 4: Parallel Nodes D, E]
    G4 --> G5[Group 5: Single Node]
    
    classDef single fill:#2196F3,color:#fff
    classDef parallel fill:#4CAF50,color:#fff
    class G1,G3,G5 single
    class G2,G4 parallel


### 10.5 Topological Sort Properties

| Property | Requirement | Verification |
|---|---|---|
| Completeness | All nodes appear in the ordering. | Count comparison |
| Validity | No node precedes its dependencies. | Dependency check |
| Stability | Equal-priority nodes maintain declaration order. | Order comparison |
| Determinism | Same graph produces same ordering. | Reproducibility test |
| Efficiency | Sorting completes within O(V+E) time. | Complexity analysis |
---

## 11 Execution Context Initialization

### 11.1 Context Hierarchy

Execution context is initialized in a hierarchical manner during the Parse and Plan phases. The hierarchy consists of four levels: Global, Workflow, Node, and Edge. Each level inherits from its parent and MAY define scoped overrides.

**Context Hierarchy Diagram:**

mermaid
graph TD
    GlobalCtx[Global Context] --> WFCtx[Workflow Context]
    WFCtx --> NodeCtx[Node Context]
    NodeCtx --> EdgeCtx[Edge Context]


### 11.2 Context Levels

| Context Level | Scope | Lifetime | Variables |
|---|---|---|---|
| Global | Entire Atlas system | Runtime lifetime | System capabilities, defaults |
| Workflow | Single workflow instance | Instance lifetime | Parameters, workflow variables |
| Node | Single node execution | Node activation lifetime | Node inputs, outputs, locals |
| Edge | Single edge traversal | Edge lifetime | Edge transformations, conditions |

### 11.3 Context Initialization Steps

| Step | Component | Description |
|---|---|---|
| 1 | Global Context | Initialize system-wide variables and capabilities. |
| 2 | Workflow Context | Initialize workflow-scoped variables and parameters. |
| 3 | Node Context | Initialize node-specific variables and resources. |
| 4 | Edge Context | Initialize edge-specific transformations and conditions. |
| 5 | Variable Bindings | Bind all declared variables to their initial values. |
| 6 | Parameter Resolution | Resolve all parameters through the resolution order. |
| 7 | Resource Allocation | Allocate all declared resources to their nodes. |



### 11.4 Context Inheritance Rules



1. Child contexts inherit all variables from parent contexts.

2. Child contexts MAY override inherited variables with scoped values.

3. Overrides MUST NOT affect the parent context.

4. Context isolation MUST be enforced: child contexts MUST NOT modify parent context variables.



### 11.5 Context Variable Scoping



| Scope | Visibility | Mutability | Lifetime |

|---|---|---|---|

| Global | All contexts | Read-only | Runtime |

| Workflow | Workflow and descendants | Read-write | Instance |

| Node | Node and descendants | Read-write | Activation |

| Edge | Edge traversal only | Read-write | Traversal |

| Local | Node body only | Read-write | Activation |



### 11.6 Context Propagation



Context variables propagate from parent to child contexts during execution. The propagation follows the context hierarchy: global to workflow, workflow to node, node to edge. Edge transformations MAY modify inherited values, and those modifications are visible to downstream nodes.



**Context Flow Diagram:**



`mermaid

sequenceDiagram

    participant GC as Global Context

    participant WC as Workflow Context

    participant NC as Node Context

    participant EC as Edge Context

    GC->>WC: Inherit global variables

    WC->>NC: Inherit workflow variables

    NC->>EC: Inherit node variables

    EC->>EC: Apply edge transformation

    EC->>NC: Return transformed data

    NC->>NC: Apply node logic

    NC->>WC: Return node result

    WC->>WC: Aggregate results

`





---



## 12 Result Propagation



### 12.1 Propagation Model



Results from node execution propagate through the execution graph via edges. When a node completes execution, its outputs are delivered to all downstream nodes that declare those outputs as inputs. The propagation follows the edge topology and respects data type compatibility constraints.



**Propagation Flow Diagram:**



`mermaid

sequenceDiagram

    participant N1 as Node Alpha

    participant E as Engine

    participant N2 as Node Beta

    participant N3 as Node Gamma

    N1->>N1: Execute

    N1->>E: Return result R1

    E->>E: Validate R1

    E->>N2: Deliver R1 as input

    E->>N3: Deliver R1 as input

    N2->>N2: Execute with R1

    N3->>N3: Execute with R1

    N2->>E: Return result R2

    N3->>E: Return result R3

`



### 12.2 Propagation Rules



| Rule | Description |

|---|---|

| Completeness | All outputs from a completed node MUST be propagated to all downstream consumers. |

| Type Safety | Propagated results MUST match the declared output types of the source node. |

| Immutability | Once propagated, results MUST NOT be modified by downstream nodes. |

| Ordering | Results MUST be propagated in dependency order. |

| Atomicity | Result propagation is atomic: either all downstream nodes receive the result, or none do. |



### 12.3 Result Types



| Result Type | Description | Propagation |

|---|---|---|

| Data | Computed output data. | Through data flow edges. |

| State | Node execution state. | Through state manager. |

| Event | Side-effect events. | Through event bus. |

| Error | Execution error information. | Through exception edges. |

| Signal | Notification signals. | Through signal edges. |



### 12.4 Propagation Verification



Each result propagation MUST be verified for:



| Verification | Description | Method |

|---|---|---|

| Existence | All declared outputs exist. | Output presence check |

| Type | Output types match declarations. | Type comparison |

| Completeness | All outputs are present. | Count verification |

| Validity | Output values satisfy constraints. | Constraint evaluation |

| Delivery | All consumers received the result. | Acknowledgment check |





---



## 13 Execution Budget Enforcement



### 13.1 Budget Components



Execution budgets constrain resource consumption during execution. The engine MUST track and enforce budgets for all declared resource types. Budgets are established during the Plan phase and monitored during the Execute phase.



| Budget Type | Unit | Enforcement Point |

|---|---|---|

| Time | Milliseconds | Per-node and per-workflow |

| Memory | Bytes | Per-node allocation |

| Compute | Processing units | Per-node and per-group |

| Network | Bytes transferred | Per-node |

| Storage | Bytes written | Per-node |

| API Calls | Count | Per-node |



### 13.2 Budget Enforcement Rules



1. The engine MUST track budget consumption for every node activation.

2. The engine MUST enforce per-node budget limits before activation.

3. The engine MUST enforce per-workflow budget limits across all nodes.

4. When a budget limit is reached, the engine MUST terminate the violating node.

5. Budget violations MUST be recorded as execution errors.

6. Budget enforcement MUST NOT compromise determinism guarantees.



### 13.3 Budget Monitoring



| Monitor | Frequency | Action on Violation |

|---|---|---|

| Time Budget | Continuous | Abort node, record violation |

| Memory Budget | Per allocation | Reject allocation, record violation |

| Compute Budget | Per operation | Limit operations, record violation |

| Network Budget | Per transfer | Block transfer, record violation |

| Storage Budget | Per write | Block write, record violation |

| API Budget | Per call | Block call, record violation |



### 13.4 Budget Hierarchy



Budgets are enforced hierarchically:



| Level | Scope | Description |

|---|---|---|

| Workflow | Entire execution | Maximum total resource consumption |

| Group | Parallel execution group | Maximum consumption per group |

| Node | Individual node | Maximum consumption per node |

| Edge | Edge traversal | Maximum data transfer per edge |



### 13.5 Budget Overflow Handling



When a budget is exceeded:



1. The engine records the violation in the execution trace.

2. The engine emits a budget violation event.

3. The engine evaluates the overflow policy:

   - **Abort**: Terminate the current node and propagate the error.

   - **Throttle**: Reduce resource consumption and continue.

   - **Escalate**: Notify the runtime scheduler for intervention.

4. The engine persists the budget state checkpoint.





---



## 14 Execution Priority



### 14.1 Priority Levels



The execution engine MUST support the following priority levels:



| Priority | Numeric Value | Description | Use Case |

|---|---|---|---|

| Critical | 0 | Highest priority; MUST execute immediately. | System-critical workflows. |

| High | 1 | High priority; executes before normal work. | Time-sensitive operations. |

| Normal | 2 | Default priority; standard scheduling. | General-purpose workflows. |

| Low | 3 | Low priority; executes when resources permit. | Background operations. |

| Idle | 4 | Lowest priority; executes only when idle. | Maintenance tasks. |



### 14.2 Priority Rules



1. Higher priority nodes MUST execute before lower priority nodes when both are ready.

2. Priority is inherited by child nodes unless explicitly overridden.

3. Priority MAY be adjusted dynamically during execution based on runtime conditions.

4. Priority adjustments MUST be recorded in the execution trace.

5. Two nodes with the same priority are ordered by the stability rule (declaration order).



### 14.3 Priority Preemption



The engine MAY preempt lower-priority nodes to accommodate higher-priority nodes:



| Condition | Action |

|---|---|

| Critical node ready | Preempt all lower-priority running nodes. |

| High node ready | Queue behind critical; preempt low and idle. |

| Normal node ready | Queue behind high and critical. |

| Low node ready | Queue behind normal, high, and critical. |

| Idle node ready | Queue behind all other priorities. |



### 14.4 Priority Inheritance



Priority inheritance ensures that resource contention does not cause priority inversion:



| Scenario | Rule |

|---|---|

| High-priority node waits for low-priority node resource | Low-priority node temporarily inherits high priority. |

| Medium-priority node ready while high waits | Medium-priority node is queued behind the high-priority chain. |

| Priority adjustment during execution | Adjustment MUST be logged and justified. |



### 14.5 Priority Scheduling Algorithm



The scheduling algorithm follows these steps:



1. Collect all Ready nodes.

2. Sort by priority (ascending numeric value = higher priority).

3. Within equal priority, sort by declaration order.

4. Select nodes whose resources are available.

5. Activate selected nodes up to the concurrency limit.





---



## 15 Resource Allocation During Execution



### 15.1 Resource Types



Resources are allocated to nodes based on their declared requirements:



| Resource Type | Allocation Unit | Scope |

|---|---|---|

| CPU | Processing units | Per-node |

| Memory | Bytes | Per-node |

| Storage | Bytes | Per-node |

| Network | Bandwidth | Per-node |

| External Services | Connections | Per-workflow |

| Custom Resources | Vendor-defined | Per-node |



### 15.2 Allocation Rules



1. Resources MUST be allocated before node activation.

2. Resources MUST be released after node completion or failure.

3. Resources allocated to one node MUST NOT be shared with another node during execution.

4. Insufficient resources MUST prevent node activation.

5. Resource allocation failures MUST trigger node failure with appropriate error.



### 15.3 Resource Lifecycle



mermaid

stateDiagram-v2

    [*] --> Unallocated

    Unallocated --> Reserved: Allocation request

    Reserved --> Allocated: Grant confirmed

    Allocated --> Released: Node completes

    Reserved --> Unallocated: Allocation denied

    Allocated --> Contended: Resource insufficient

    Contended --> Released: Wait timeout

    Contended --> Allocated: Resource freed





### 15.4 Resource Reservation



Resources follow a reservation-based allocation model:



| Stage | Description | Timeout |

|---|---|---|

| Request | Node declares resource requirements. | Immediate |

| Reserved | Resources are tentatively held. | Configurable |

| Allocated | Resources are confirmed for use. | Node lifetime |

| Released | Resources are returned to the pool. | Immediate |

| Contended | Multiple nodes request same resource. | Configurable |



### 15.5 Resource Contention Resolution



When resources are contended:



1. The engine identifies all requesting nodes.

2. The engine applies priority ordering to the requests.

3. Higher-priority requests are granted first.

4. Lower-priority requests are queued or denied.

5. Denied requests trigger a resource shortage error.





---



## 16 Execution Fault Tolerance



### 16.1 Failure Classification



Failures during execution are classified as:



| Failure Type | Description | Recovery |

|---|---|---|

| Transient | Temporary failure that may resolve. | Retry with backoff. |

| Permanent | Failure that will not resolve. | Skip or compensate. |

| Resource | Resource exhaustion or unavailability. | Wait or fail. |

| Data | Invalid or missing data. | Error handler. |

| Condition | Condition evaluation failure. | Default path or error. |

| Timeout | Execution exceeded time budget. | Abort and compensate. |



### 16.2 Retry Policy



The engine MUST support configurable retry policies:



| Policy Parameter | Description | Default |

|---|---|---|

| Max Retries | Maximum number of retry attempts. | 3 |

| Backoff Strategy | Strategy for delay between retries. | Exponential |

| Backoff Base | Base delay in milliseconds. | 1000 |

| Backoff Max | Maximum delay between retries. | 30000 |

| Retryable Errors | Set of error types eligible for retry. | Transient, Resource |



### 16.3 Checkpointing



The engine MUST create checkpoints at defined boundaries:



| Checkpoint Type | Trigger | Content |

|---|---|---|

| Node Checkpoint | After each node completion. | Node state, outputs, context. |

| Phase Checkpoint | After each phase completion. | Phase state, graph state. |

| Group Checkpoint | After each parallel group completion. | Group state, aggregated results. |

| Manual Checkpoint | Upon explicit request. | Full execution state. |



### 16.4 Checkpoint Format



Each checkpoint MUST contain:



| Field | Description |

|---|---|

| Checkpoint ID | Unique identifier for the checkpoint. |

| Timestamp | Wall-clock time of checkpoint creation. |

| Phase | Current execution phase. |

| Node States | State of every node in the graph. |

| Edge States | State of every edge in the graph. |

| Context Snapshot | Full execution context at checkpoint time. |

| Result Store | All accumulated results up to checkpoint. |

| Budget State | Remaining budget for each resource type. |



### 16.5 Recovery Procedure



When recovering from a checkpoint:



1. Load the checkpoint from persistent storage.

2. Validate the checkpoint integrity.

3. Restore the execution context from the checkpoint.

4. Restore all node and edge states.

5. Resume execution from the recovery point.

6. Emit a recovery event to the event bus.





---



## 17 Observability During Execution



### 17.1 Observable Elements



The following elements MUST be observable during execution:



| Element | Observable Property | Event Emitted |

|---|---|---|

| Node Activation | Start time, node ID, priority. | NodeStarted |

| Node Completion | End time, result summary. | NodeCompleted |

| Node Failure | Failure reason, error code. | NodeFailed |

| Edge Traversal | Source node, target node, data type. | EdgeTriggered |

| Condition Evaluation | Condition expression, result. | ConditionEvaluated |

| Budget Consumption | Resource type, amount consumed. | BudgetConsumed |

| Checkpoint | Checkpoint type, timestamp. | CheckpointCreated |

| Retry | Retry count, backoff duration. | RetryAttempted |



### 17.2 Execution Trace



The execution trace records every execution step in a deterministic format:



| Trace Entry | Fields |

|---|---|

| Phase Transition | From phase, to phase, timestamp |

| Node Activation | Node ID, start time, priority, inputs |

| Node Completion | Node ID, end time, outputs, duration |

| Node Failure | Node ID, failure reason, error code, stack |

| Edge Traversal | Source node, target node, data payload hash |

| Condition Evaluation | Condition ID, expression, result, duration |

| Budget Update | Resource type, amount, remaining |

| Checkpoint | Checkpoint ID, type, size, timestamp |



### 17.3 Trace Format



Execution traces MUST conform to the following format requirements:



| Requirement | Description |

|---|---|

| Immutable | Trace entries MUST NOT be modified after recording. |

| Append-only | Entries MUST only be appended; no insertions or deletions. |

| Timestamped | Every entry MUST have a monotonic timestamp. |

| Ordered | Entries MUST be ordered by timestamp. |

| Indexed | Entries MUST be indexed by node ID, edge ID, and phase. |

| Searchable | Traces MUST support filtering by entry type and entity ID. |



### 17.4 Observability Interfaces



The engine MUST expose observability data through:



| Interface | Purpose | Access |

|---|---|---|

| Event Bus | Real-time event emission. | All subscribers |

| Trace Store | Persistent trace storage. | Query interface |

| State Store | Current execution state. | Read interface |

| Metrics Collector | Resource and performance metrics. | Aggregation interface |

| Audit Log | Immutable audit trail. | Append-only log |





---



## 18 Concurrency and Parallelism in Execution



### 18.1 Parallelism Strategies



The execution engine MUST support the following parallelism strategies:



| Strategy | Description | Use Case |

|---|---|---|

| Independent | Nodes with no dependencies execute in parallel. | Fan-out patterns. |

| Pipeline | Stages of a pipeline execute concurrently. | Data processing chains. |

| Batch | Multiple instances of the same node execute in parallel. | Mass operations. |

| Adaptive | Parallelism adjusts based on resource availability. | Dynamic environments. |

| Constrained | Parallelism is limited by explicit concurrency bounds. | Resource-constrained environments. |



### 18.2 Concurrency Controls



| Control | Description | Enforcement |

|---|---|---|

| Max Concurrent Nodes | Maximum number of simultaneously running nodes. | Scheduler |

| Max Concurrent Groups | Maximum number of simultaneously active parallel groups. | Engine |

| Resource Lock | Prevents simultaneous access to shared resources. | Resource manager |

| Race Resolution | Deterministic resolution of concurrent data access. | Engine |



### 18.3 Race Condition Prevention



The engine MUST prevent race conditions through:



1. **Dependency Enforcement**: Nodes MUST NOT read outputs from nodes that have not yet completed.

2. **Write Serialization**: Concurrent writes to the same context variable MUST be serialized.

3. **Read-After-Write Consistency**: Reads MUST observe the most recent write.

4. **Atomic Commits**: Node result commits are atomic with respect to dependent reads.



### 18.4 Parallelism Verification



| Verification | Description | Method |

|---|---|---|

| Independence | Confirmed no interdependencies within parallel groups. | Graph analysis |

| Equivalence | All interleavings produce equivalent states. | State comparison |

| Completeness | All parallel paths complete or fail. | Path coverage |

| Consistency | Shared state is consistent after parallel execution. | State verification |





---



## 19 Execution Verification



### 19.1 Verification Points



The engine MUST verify execution correctness at the following points:



| Verification Point | What is Verified | Action on Failure |

|---|---|---|

| Post-Parse | Graph structure integrity. | Reject definition. |

| Post-Validate | All invariants satisfied. | Reject definition. |

| Post-Plan | Execution plan is valid. | Regenerate plan. |

| Post-Activate | Node inputs are complete. | Wait or fail. |

| Post-Complete | Node outputs are valid. | Record error. |

| Post-Propagate | Results reach all consumers. | Retry propagation. |

| Post-Checkpoint | Checkpoint is restorable. | Regenerate checkpoint. |



### 19.2 Verification Methods



| Method | Description | Applicability |

|---|---|---|

| Structural | Verify graph topology. | Parse, Validate phases. |

| Semantic | Verify data type consistency. | Validate phase. |

| Runtime | Verify execution state invariants. | Execute phase. |

| Post-hoc | Verify final state correctness. | Complete phase. |

| Replay | Verify trace reproducibility. | Any phase. |



### 19.3 Verification Orchestration



Verification is orchestrated as follows:



mermaid

flowchart TD

    Parse[Parse] --> Ver1{Parse Verified?}

    Ver1 -->|Yes| Validate[Validate]

    Ver1 -->|No| Reject1[Reject Definition]

    Validate --> Ver2{Valid?}

    Ver2 -->|Yes| Plan[Plan]

    Ver2 -->|No| Reject2[Reject Definition]

    Plan --> Ver3{Plan Valid?}

    Ver3 -->|Yes| Execute[Execute]

    Ver3 -->|No| Regenerate[Regenerate Plan]

    Execute --> Ver4{Execution Correct?}

    Ver4 -->|Yes| Complete[Complete]

    Ver4 -->|No| ErrorHandle[Error Handling]

    Complete --> Ver5{Final State Valid?}

    Ver5 -->|Yes| Terminate[Terminate]

    Ver5 -->|No| Rollback[Rollback]







---



## 20 Acceptance Criteria



### 20.1 Execution Graph Model



| # | Criterion | Verification Method |

|---|---|---|

| AC-01 | The execution graph MUST be a directed acyclic graph. | Graph analysis test |

| AC-02 | All nodes MUST be reachable from at least one entry node. | Reachability test |

| AC-03 | All nodes MUST be able to reach at least one exit node. | Reverse reachability test |

| AC-04 | Six execution invariants MUST be enforced. | Invariant test suite |

| AC-05 | The graph representation MUST include vertices, edges, and metadata. | Structure verification |



### 20.2 Execution Phases



| # | Criterion | Verification Method |

|---|---|---|

| AC-06 | Six execution phases MUST be supported. | Phase enumeration test |

| AC-07 | Phases MUST proceed in the defined order: Parse, Validate, Plan, Execute, Complete, Terminate. | Phase order test |

| AC-08 | No phase MAY be skipped. | Phase skipping test |

| AC-09 | Parse phase MUST produce a complete execution graph AST. | AST completeness test |

| AC-10 | Validate phase MUST enforce all twelve validation rules. | Validation test suite |

| AC-11 | Plan phase MUST produce execution order, parallel groups, resource allocation, and budget assignments. | Plan completeness test |

| AC-12 | Execute phase MUST activate nodes in dependency order. | Activation order test |

| AC-13 | Complete phase MUST aggregate all node results. | Aggregation test |

| AC-14 | Terminate phase MUST release all resources. | Resource release test |



### 20.3 Node Execution Semantics



| # | Criterion | Verification Method |

|---|---|---|

| AC-15 | Eight node activation steps MUST be performed in order. | Step enumeration test |

| AC-16 | Eight node execution states MUST be supported. | State enumeration test |

| AC-17 | Ten node types MUST have defined execution semantics. | Semantics test |

| AC-18 | Node precondition evaluation MUST occur before execution. | Precondition test |

| AC-19 | Resource acquisition MUST occur before node execution. | Resource test |



### 20.4 Edge Traversal



| # | Criterion | Verification Method |

|---|---|---|

| AC-20 | Six edge types MUST be supported. | Edge type enumeration test |

| AC-21 | Six edge states MUST be supported. | Edge state enumeration test |

| AC-22 | Dependency resolution MUST follow the defined algorithm. | Resolution test |

| AC-23 | Dependency resolution table MUST have all five rows. | Table verification |



### 20.5 Determinism



| # | Criterion | Verification Method |

|---|---|---|

| AC-24 | Same definition and context MUST produce identical execution traces. | Determinism test |

| AC-25 | Same inputs MUST produce identical node outputs. | Output comparison test |

| AC-26 | Same conditions MUST produce identical path traversal. | Path comparison test |

| AC-27 | Four sources of non-determinism MUST have documented mitigations. | Mitigation verification |

| AC-28 | Three determinism verification methods MUST be supported. | Method enumeration test |



### 20.6 Topological Sort



| # | Criterion | Verification Method |

|---|---|---|

| AC-29 | Topological ordering MUST respect all dependency relationships. | Ordering test |

| AC-30 | Topological ordering MUST be stable for equal-priority nodes. | Stability test |

| AC-31 | Topological ordering MUST be unique for given inputs. | Uniqueness test |

| AC-32 | Four execution ordering rules MUST be enforced. | Rule enforcement test |

| AC-33 | Parallel execution groups MUST satisfy independence and atomicity rules. | Group test |



### 20.7 Context Initialization



| # | Criterion | Verification Method |

|---|---|---|

| AC-34 | Four context levels MUST be initialized in hierarchy: global, workflow, node, edge. | Context hierarchy test |

| AC-35 | Seven context initialization steps MUST be performed. | Step enumeration test |

| AC-36 | Three context inheritance rules MUST be enforced. | Inheritance test |



### 20.8 Result Propagation



| # | Criterion | Verification Method |

|---|---|---|

| AC-37 | Five result propagation rules MUST be enforced. | Rule enforcement test |

| AC-38 | Five result types MUST be supported. | Result type enumeration test |

| AC-39 | All outputs from a completed node MUST reach all downstream consumers. | Propagation completeness test |



### 20.9 Budget Enforcement



| # | Criterion | Verification Method |

|---|---|---|

| AC-40 | Six budget types MUST be supported. | Budget type enumeration test |

| AC-41 | Six budget enforcement rules MUST be enforced. | Rule enforcement test |

| AC-42 | Six budget monitors MUST be implemented. | Monitor enumeration test |



### 20.10 Priority



| # | Criterion | Verification Method |

|---|---|---|

| AC-43 | Five priority levels MUST be supported. | Priority enumeration test |

| AC-44 | Five priority rules MUST be enforced. | Rule enforcement test |

| AC-45 | Priority preemption MUST follow the defined table. | Preemption test |



### 20.11 Resource Allocation



| # | Criterion | Verification Method |

|---|---|---|

| AC-46 | Six resource types MUST be supported. | Resource type enumeration test |

| AC-47 | Five resource allocation rules MUST be enforced. | Rule enforcement test |

| AC-48 | Resource lifecycle MUST support all seven states. | Lifecycle state enumeration test |



### 20.12 Fault Tolerance



| # | Criterion | Verification Method |

|---|---|---|

| AC-49 | Six failure types MUST be classified. | Failure classification test |

| AC-50 | Six retry policy parameters MUST be configurable. | Policy configuration test |

| AC-51 | Four checkpoint types MUST be supported. | Checkpoint type enumeration test |



### 20.13 Observability



| # | Criterion | Verification Method |

|---|---|---|

| AC-52 | Eight observable elements MUST be exposed. | Element enumeration test |

| AC-53 | Eight trace entry types MUST be recorded. | Trace entry enumeration test |



### 20.14 Concurrency



| # | Criterion | Verification Method |

|---|---|---|

| AC-54 | Five parallelism strategies MUST be supported. | Strategy enumeration test |

| AC-55 | Four concurrency controls MUST be implemented. | Control implementation test |

| AC-56 | Four race condition prevention mechanisms MUST be enforced. | Mechanism test |





---



## 21 References



| Reference | Description |

|---|---|

| RFC-0001 | Runtime Overview |

| RFC-0002 | Runtime Lifecycle |

| RFC-0003 | Runtime Service Model |

| RFC-0004 | Runtime Scheduler |

| RFC-0005 | Runtime Event Bus |

| RFC-0006 | Runtime State Management |

| RFC-0301 | Workflow Overview |

| RFC-0302 | Workflow Language |

| RFC-0304 | Workflow Runtime |

| RFC-0305 | Workflow Lifecycle |

| RFC-0306 | Workflow State |

| RFC-0307 | Workflow Context |

| RFC-0308 | Workflow Events |

| RFC-0309 | Workflow Actions |

| RFC-0310 | Workflow Conditions |

| RFC-0313 | Workflow Parallelism |

| RFC-0314 | Workflow Error Handling |

| RFC-0320 | Workflow Performance |

| RFC-0321 | Workflow Observability |

| RFC-1001 | Common Event Model |

| RFC-1002 | Common State Model |

| RFC-1003 | Common Capability Model |

| RFC-1004 | Common Contract Model |

| RFC-1005 | Common Manifest Model |

| RFC-1006 | Common Error Model |

| ADR-0012 | Contract-First Specification-Driven Development |

| Glossary | Atlas Master Glossary |

| Constitution | Atlas AI Constitution |



---



## 22 Changelog



| Version | Date | Change |

|---|---|---|

| 1.0.0 | 2026-07-01 | Initial specification. Defined execution graph model, six execution phases, node semantics, edge traversal, determinism guarantees, topological sort, context initialization, result propagation, budget enforcement, priority, resource allocation, fault tolerance, observability, and concurrency. |



---



## 23 Compatibility



This specification is compatible with Spec 1.x. All implementations MUST conform to the requirements defined herein to achieve compatibility certification.


---

## 40 Terminology

| Term | Definition | Source |
|---|---|---|
| Execution | The process of evaluating and completing a workflow graph according to the language model. | RFC-0301 |
| Execution Engine | The component responsible for evaluating workflow graphs and activating nodes. | This RFC |
| Result Propagation | The mechanism by which node outputs become inputs for downstream nodes. | This RFC |
| Execution State | The current position and data within a workflow graph during execution. | This RFC |
| Deterministic Execution | Execution that produces identical results for identical inputs. | RFC-0301 |
| Node Activation | The process of preparing and initiating a node's work. | This RFC |

## 41 Layer Boundaries

### 41.1 Responsibilities
This specification IS responsible for: defining the execution model, specifying the execution engine contract, defining result propagation semantics, and establishing execution state management.

### 41.2 Non-Responsibilities
This specification IS NOT responsible for: scheduling execution (delegated to RFC-0312), hosting the runtime (delegated to RFC-0304), persisting state (delegated to RFC-0324), or observing execution (delegated to RFC-0321).

### 41.3 Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |
| RFC-0302 | Consumed | Workflow Language provides the definition model |
| RFC-0304 | Consumed | Workflow Runtime provides the hosting layer |
| RFC-0305 | Consumed | Workflow Lifecycle provides lifecycle integration |
| RFC-0306 | Consumed | Workflow State provides state model |
| RFC-0312 | Consumed | Workflow Scheduler provides scheduling decisions |
| RFC-0313 | Consumed | Workflow Parallelism provides parallel execution |
| RFC-0314 | Consumed | Workflow Error Handling provides error semantics |
| RFC-0315 | Consumed | Workflow Recovery provides recovery semantics |
| RFC-0316 | Consumed | Workflow Debugging provides debug hooks |
| RFC-0319 | Consumed | Workflow Security provides execution security |
| RFC-0320 | Consumed | Workflow Performance provides performance model |
| RFC-0321 | Consumed | Workflow Observability provides execution telemetry |
| RFC-0324 | Consumed | Workflow Storage provides state persistence |

### 41.4 Consumers
- Workflow Runtime (RFC-0304): Hosts the execution engine.
- Workflow Scheduler (RFC-0312): Receives scheduling decisions from execution.
- Workflow Parallelism (RFC-0313): Coordinates parallel execution with execution engine.
- Workflow Recovery (RFC-0315): Restores execution state on failure.

### 41.5 Providers
- Execution State Schema (schemas/workflow/execution-state.json): Provides the execution state format.
- Result Propagation Schema (schemas/workflow/result-propagation.json): Provides the result format.
- Result Types Catalog (catalog/workflow-result-types.md): Provides the result type taxonomy.
- Status Catalog (catalog/workflow-status.md): Provides the status code taxonomy.

### 41.6 Forbidden Dependencies
- This specification MUST NOT depend on any specific execution engine implementation.
- This specification MUST NOT assume a particular scheduling algorithm.

## 42 Future Evolution
- **Distributed Execution**: Execution across multiple runtime instances.
- **Edge Execution**: Execution at the network edge for low-latency requirements.
- **Federated Execution**: Cross-organization workflow execution with security boundaries.
- **AI-Driven Execution**: ML-optimized execution strategies based on historical data.

## 43 Runtime Independence
This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:
- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)

## 44 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0302 | Workflow Language (definition model) |
| RFC-0304 | Workflow Runtime (execution hosting) |
| RFC-0305 | Workflow Lifecycle (lifecycle integration) |
| RFC-0306 | Workflow State (state model) |
| RFC-0312 | Workflow Scheduler (scheduling decisions) |
| RFC-0313 | Workflow Parallelism (parallel execution) |
| RFC-0314 | Workflow Error Handling (error semantics) |
| RFC-0315 | Workflow Recovery (recovery semantics) |
| RFC-0316 | Workflow Debugging (debug hooks) |
| RFC-0319 | Workflow Security (execution security) |
| RFC-0320 | Workflow Performance (performance model) |
| RFC-0321 | Workflow Observability (execution telemetry) |
| RFC-0324 | Workflow Storage (state persistence) |
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/execution-state.json | Execution State JSON Schema |
| schemas/workflow/result-propagation.json | Result Propagation JSON Schema |
| catalog/workflow-result-types.md | Result Types Catalog |
| catalog/workflow-status.md | Status Catalog |
| catalog/workflow-actions.md | Actions Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0303 (this document), RFC-0301 (Overview), RFC-0304 (Runtime) |
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
