# Atlas Vision Runtime Documentation

## Overview

The Atlas Vision Runtime provides platform-independent image acquisition,
frame processing, computer vision pipelines, provider abstraction, and
deterministic execution.

## Components

- [Frame Model](vision/) — Immutable frame data structures
- [Capture Abstraction](vision/) — Platform-independent capture sources
- [Vision Pipeline](vision/) — Deterministic composable processing stages
- [Provider Abstraction](vision/) — Plugin-based vision processing
- [Vision Registry](vision/) — Service, provider, and capability registries
- [Graph Execution](vision/) — Deterministic DAG planning
- [Scheduler](vision/) — Multi-trigger task scheduling
- [Resources](vision/) — LRU caching and buffer management
- [Metrics](vision/) — Counters, gauges, histograms
- [Health](vision/) — Runtime health monitoring
- [Security](vision/) — Permission validation and isolation
- [Storage](vision/) — Abstract persistence
- [Integration](vision/) — IPC, Workflow, Plugin bridges

## Architecture Compliance

See [VISION_COMPLIANCE_REPORT.md](VISION_COMPLIANCE_REPORT.md) for full RFC mapping
and acceptance criteria verification.
