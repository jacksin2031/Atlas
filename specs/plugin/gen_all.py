import os, sys

base = r"E:\u8cc7\u6599\u593e\u684c\u9762\Atlas\specs\plugin"

def w(name, content):
    p = os.path.join(base, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK {name} ({len(content)} bytes)")


rfc0215_header = '''# RFC-0215: Plugin Service Model

RFC: RFC-0215
Title: Plugin Service Model
Status: Proposed
Version: 0.1.0
Category: Plugin
Layer: Extension
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0203 Plugin Lifecycle
  - RFC-0205 Plugin Registry
  - RFC-0209 Plugin API
  - RFC-1001 Common Event Model
  - RFC-1003 Common Capability Model
Related RFC:
  - RFC-0204 Plugin Loader
  - RFC-0206 Plugin Capability
  - RFC-0210 Plugin Events
  - RFC-0211 Plugin Dependency
Related ADR:
  - ADR-0005 Plugin Architecture
  - ADR-0014 Extension Point Architecture
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

This specification is Normative. Every Atlas implementation MUST conform to the service registration, service lifetime, service scope, service registry, service resolution, dependency injection, service lifecycle, inter-service communication, and error handling defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Service Philosophy](#4-service-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Service Registration](#9-service-registration)
10. [Service Lifetime](#10-service-lifetime)
11. [Service Scope](#11-service-scope)
12. [Service Registry](#12-service-registry)
13. [Service Resolution](#13-service-resolution)
14. [Dependency Injection](#14-dependency-injection)
15. [Service Lifecycle](#15-service-lifecycle)
16. [Inter-Service Communication](#16-inter-service-communication)
17. [Error Handling](#17-error-handling)
18. [Performance Budgets](#18-performance-budgets)
19. [Glossary](#19-glossary)
20. [Acceptance Criteria](#20-acceptance-criteria)
21. [Cross References](#21-cross-references)
22. [References](#22-references)
23. [Revision History](#23-revision-history)
24. [Future Evolution](#24-future-evolution)

'''
