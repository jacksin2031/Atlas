from __future__ import annotations

import pytest

from atlas_automation import reference_bundle, resolve_reference_point


def test_provider_match_normalizes_to_all_reference_shapes() -> None:
    refs = reference_bundle(
        {"x": 100, "y": 200, "width": 80, "height": 40, "confidence": 0.94, "label": "button"},
        {"frameId": "frame-1"},
        "detect",
    )

    assert refs["region"]["referenceType"] == "region"
    assert refs["bounds"]["referenceType"] == "bounds"
    assert refs["point"] == {
        "contract": "atlas.automation.reference/v1",
        "referenceType": "point",
        "coordinateSpace": "screen",
        "x": 140,
        "y": 220,
        "sourceFrameId": "frame-1",
        "confidence": 0.94,
        "label": "button",
    }
    assert resolve_reference_point(refs["region"]) == (140, 220)
    assert resolve_reference_point(refs["bounds"]) == (140, 220)
    assert resolve_reference_point(refs["point"]) == (140, 220)


def test_input_rejects_non_screen_typed_reference() -> None:
    with pytest.raises(ValueError, match="screen-space"):
        resolve_reference_point({"referenceType": "point", "coordinateSpace": "frame", "x": 1, "y": 2})
