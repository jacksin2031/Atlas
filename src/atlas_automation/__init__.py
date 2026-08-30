"""Shared contracts for Atlas desktop automation domains."""

from .references import (
    BoundsReference,
    PointReference,
    RegionReference,
    reference_bundle,
    resolve_reference_point,
)

__all__ = [
    "BoundsReference",
    "PointReference",
    "RegionReference",
    "reference_bundle",
    "resolve_reference_point",
]
