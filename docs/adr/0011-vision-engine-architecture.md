# ADR-0011: Vision Engine Architecture

Status: Accepted

Date: 2026-06-28

Authors:
Atlas Core Team

Supersedes:
None

Superseded By:
None

---

# Context

Atlas is designed to automate desktop applications and games by understanding visual content rather than relying solely on APIs or fixed UI selectors.

The Vision Engine is responsible for converting screen pixels into structured semantic information that can be consumed by the Workflow Engine, Recorder, AI Operating System (AIOS), and Plugins.

Vision is a foundational capability and SHALL be treated as a first-class platform service.

---

# Problem Statement

Traditional automation tools depend on:

- Fixed window coordinates
- Pixel colors
- Accessibility APIs
- DOM selectors
- Memory reading

These approaches are often fragile, application-specific, and incompatible with many games or custom interfaces.

Atlas requires a generalized visual understanding layer that works across desktop applications regardless of implementation.

---

# Decision

Atlas SHALL implement a modular Vision Engine responsible for all visual perception tasks.

All visual operations SHALL be performed through the Vision Engine.

No subsystem SHALL directly process screen images outside this architecture.

---

# Vision Principles

The Vision Engine SHALL be:

- Modular
- Extensible
- Provider-independent
- Hardware-aware
- Real-time capable
- GPU-accelerated when available
- Cross-platform
- Deterministic where possible

---

# Responsibilities

The Vision Engine SHALL provide:

- Screen Capture
- Region Capture
- Window Detection
- OCR
- Template Matching
- Object Detection
- Image Classification
- UI Detection
- Icon Recognition
- Color Analysis
- Motion Detection
- Image Comparison

These services SHALL be independently replaceable.

---

# Architecture

The Vision Engine SHALL consist of:

- Capture Manager
- Frame Pipeline
- Image Preprocessor
- OCR Engine
- Detection Engine
- Matching Engine
- Tracking Engine
- Vision Cache
- Hardware Manager
- Result Dispatcher

Each module SHALL communicate through internal contracts.

---

# Capture Pipeline

The standard pipeline SHALL be:

Screen

↓

Capture

↓

Preprocessing

↓

Detection

↓

OCR

↓

Semantic Analysis

↓

Structured Results

↓

Workflow Engine

Every processing stage SHALL remain replaceable.

---

# Capture Sources

Supported capture sources SHALL include:

- Full Desktop
- Application Window
- Monitor
- Region
- Virtual Display
- Recorded Video
- Image File

Future capture providers SHALL require no architectural redesign.

---

# OCR

OCR SHALL support:

- Multiple Languages
- Vertical Text
- Mixed Languages
- Numbers
- Symbols

OCR providers SHALL be interchangeable.

Examples:

- PaddleOCR
- Tesseract
- Windows OCR
- Cloud OCR

---

# Object Detection

The engine SHALL support:

- YOLO
- ONNX Models
- OpenCV
- Custom Models

Detected objects SHALL include:

Bounding Box

Confidence

Class

Tracking ID

Timestamp

---

# UI Detection

The Vision Engine SHALL identify:

Buttons

Menus

Icons

Progress Bars

Health Bars

Mini Maps

Inventory Slots

Dialogs

Text Fields

Check Boxes

Scroll Bars

Detection SHALL remain independent of operating systems.

---

# Template Matching

Atlas SHALL support:

Exact Matching

Multi-scale Matching

Rotation Matching

Partial Matching

Template collections SHALL be reusable across workflows.

---

# Motion Detection

The engine SHALL support:

Frame Difference

Optical Flow

Motion Regions

Object Tracking

Motion SHALL be available as workflow events.

---

# Image Comparison

Supported comparison algorithms SHALL include:

Pixel Difference

Structural Similarity (SSIM)

Perceptual Hash

Feature Matching

Comparison SHALL support configurable thresholds.

---

# Vision Cache

Repeated analysis SHALL be cached.

Cacheable items include:

OCR Results

Templates

Detection Results

Feature Maps

Frame Hashes

The cache SHALL use configurable expiration policies.

---

# Hardware Acceleration

The engine SHALL automatically detect available hardware.

Supported execution targets:

CPU

GPU

CUDA

DirectML

Metal

Vulkan

Execution SHALL gracefully fall back to CPU.

---

# AI Integration

The Vision Engine MAY delegate advanced analysis to AI providers.

Examples:

Scene Understanding

Document Parsing

UI Description

Image Captioning

Object Reasoning

All AI requests SHALL pass through the AIOS.

---

# Workflow Integration

Workflow Nodes SHALL consume structured vision outputs.

Nodes SHALL never perform raw image analysis.

Example:

Capture Screen

↓

Find Health Bar

↓

Read HP Value

↓

Decision Node

↓

Execute Action

---

# Recorder Integration

Recorder SHALL record:

Frames

Mouse

Keyboard

Window State

Vision Events

These recordings SHALL enable replay and workflow generation.

---

# Plugin Integration

Plugins MAY register:

Vision Providers

OCR Providers

Detection Models

Custom Matchers

Plugins SHALL implement the Vision Provider Interface.

---

# Performance Targets

Target capture rate:

30–60 FPS

OCR latency:

<100 ms per region

Template Matching:

<20 ms

Detection latency:

Configurable by model

Vision processing SHALL avoid blocking the UI thread.

---

# Security

Vision SHALL never access:

Protected OS memory

Kernel APIs

Application internals

Vision SHALL only analyze rendered pixels unless explicitly authorized.

---

# Logging

Vision operations SHALL log:

Frame ID

Capture Source

Execution Time

Provider

Errors

Hardware Backend

Logs SHALL omit image data unless debugging is enabled.

---

# Monitoring

Metrics SHALL include:

FPS

Detection Latency

OCR Accuracy

GPU Usage

Memory Usage

Dropped Frames

These metrics SHALL be visible through developer tools.

---

# Future Extensions

The architecture SHALL support:

3D Scene Understanding

Video Segmentation

Pose Detection

Gesture Recognition

Depth Estimation

AR Integration

Eye Tracking

No redesign shall be required.

---

# Alternatives Considered

## OpenCV-only

Pros

Simple.

Cons

Limited semantics.

Rejected.

---

## AI-only Vision

Pros

High capability.

Cons

High cost.

High latency.

Rejected.

---

## Hybrid Vision Architecture

Pros

Fast.

Modular.

Offline capable.

Future-proof.

Accepted.

---

# Consequences

## Positive

Generalized automation.

Cross-platform compatibility.

AI-ready architecture.

Plugin extensibility.

Offline support.

High performance.

## Negative

Increased implementation complexity.

Requires model management.

Hardware optimization needed.

---

# Risks

Poor OCR accuracy.

False detections.

GPU incompatibilities.

Model drift.

---

# Mitigations

Provider abstraction.

Confidence thresholds.

Hardware fallback.

Continuous benchmarking.

---

# Implementation Notes

Implementation SHALL reside under:

packages/vision/

Suggested modules:

capture/

pipeline/

ocr/

detector/

matcher/

tracker/

cache/

providers/

hardware/

dispatcher/

All vision functionality SHALL remain isolated from workflow execution.

---

# Related ADRs

ADR-0005 Plugin Architecture

ADR-0006 Workflow Engine

ADR-0007 Knowledge Pack System

ADR-0008 AI Provider Independence

ADR-0009 AI Routing & Model Orchestration

ADR-0010 IPC & Runtime Architecture

ADR-0012 Contract-First Development

---

# Related Specifications

specs/vision/

specs/runtime/

specs/workflow/

contracts/json/vision.schema.json

---

# References

OpenCV

PaddleOCR

Tesseract OCR

ONNX Runtime

YOLO

MediaPipe

DirectML

CUDA

Metal Performance Shaders

Windows Graphics Capture API
