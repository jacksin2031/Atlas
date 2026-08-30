"""Provider-neutral typed references shared by Vision and Input runtimes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


CoordinateSpace = Literal["screen"]
CONTRACT = "atlas.automation.reference/v1"


@dataclass(frozen=True)
class PointReference:
    x: int
    y: int
    source_frame_id: str
    confidence: float = 1.0
    label: str = "target"
    coordinate_space: CoordinateSpace = "screen"

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": CONTRACT,
            "referenceType": "point",
            "coordinateSpace": self.coordinate_space,
            "x": self.x,
            "y": self.y,
            "sourceFrameId": self.source_frame_id,
            "confidence": self.confidence,
            "label": self.label,
        }


@dataclass(frozen=True)
class BoundsReference:
    x: int
    y: int
    width: int
    height: int
    source_frame_id: str
    confidence: float = 1.0
    label: str = "target"
    coordinate_space: CoordinateSpace = "screen"

    @property
    def center(self) -> PointReference:
        return PointReference(
            self.x + self.width // 2,
            self.y + self.height // 2,
            self.source_frame_id,
            self.confidence,
            self.label,
            self.coordinate_space,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": CONTRACT,
            "referenceType": "bounds",
            "coordinateSpace": self.coordinate_space,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "sourceFrameId": self.source_frame_id,
            "confidence": self.confidence,
            "label": self.label,
            "center": self.center.to_dict(),
        }


@dataclass(frozen=True)
class RegionReference:
    region_id: str
    bounds: BoundsReference

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": CONTRACT,
            "referenceType": "region",
            "coordinateSpace": self.bounds.coordinate_space,
            "regionId": self.region_id,
            "sourceFrameId": self.bounds.source_frame_id,
            "confidence": self.bounds.confidence,
            "label": self.bounds.label,
            "bounds": self.bounds.to_dict(),
            "center": self.bounds.center.to_dict(),
        }


def _number(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Reference {name} must be numeric")
    return int(value)


def reference_bundle(match: dict[str, Any], frame: dict[str, Any], node_id: str) -> dict[str, dict[str, Any]]:
    """Normalize one provider match into all three Atlas reference shapes."""
    raw_bounds = match.get("bounds", match)
    if not isinstance(raw_bounds, dict):
        raise ValueError("Vision provider result is missing bounds")
    frame_id = str(match.get("sourceFrameId") or frame.get("frameId") or frame.get("id") or "unknown-frame")
    confidence = max(0.0, min(float(match.get("confidence", 1.0)), 1.0))
    label = str(match.get("label") or match.get("text") or match.get("className") or "target")
    bounds = BoundsReference(
        _number(raw_bounds.get("x"), "x"),
        _number(raw_bounds.get("y"), "y"),
        max(1, _number(raw_bounds.get("width"), "width")),
        max(1, _number(raw_bounds.get("height"), "height")),
        frame_id,
        confidence,
        label,
    )
    region_id = str(match.get("regionId") or f"{node_id}:{frame_id}:{bounds.x}:{bounds.y}:{bounds.width}:{bounds.height}")
    return {
        "region": RegionReference(region_id, bounds).to_dict(),
        "bounds": bounds.to_dict(),
        "point": bounds.center.to_dict(),
    }


def resolve_reference_point(value: Any) -> tuple[int, int] | None:
    """Resolve an Atlas typed reference (or legacy coordinate object) to a screen point."""
    if not isinstance(value, dict):
        return None
    reference_type = value.get("referenceType")
    if reference_type and value.get("coordinateSpace", "screen") != "screen":
        raise ValueError("Input Runtime only accepts screen-space target references")
    if reference_type == "region":
        return resolve_reference_point(value.get("bounds") or value.get("center"))
    if reference_type == "bounds":
        x, y = _number(value.get("x"), "x"), _number(value.get("y"), "y")
        return x + _number(value.get("width"), "width") // 2, y + _number(value.get("height"), "height") // 2
    if reference_type == "point":
        return _number(value.get("x"), "x"), _number(value.get("y"), "y")
    for nested in ("region", "bounds", "target", "center"):
        if nested in value:
            resolved = resolve_reference_point(value[nested])
            if resolved:
                return resolved
    if "x" not in value or "y" not in value:
        return None
    x, y = _number(value.get("x"), "x"), _number(value.get("y"), "y")
    if "width" in value and "height" in value:
        return x + _number(value.get("width"), "width") // 2, y + _number(value.get("height"), "height") // 2
    return x, y
