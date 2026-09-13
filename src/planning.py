"""Manifest validation and liquid-volume planning."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

REQUIRED_COLUMNS = {
    "sample_id",
    "source_well",
    "plate_row",
    "source_volume_ul",
    "dead_volume_ul",
}
VALID_SOURCE_WELLS = {
    f"{row}{column}" for row in "ABCD" for column in range(1, 7)
}
VALID_PLATE_ROWS = set("ABCDEFGH")


@dataclass(frozen=True)
class Sample:
    sample_id: str
    source_well: str
    plate_row: str
    source_volume_ul: float
    dead_volume_ul: float


def load_manifest(path: str | Path) -> list[Sample]:
    """Load and validate an eight-sample-or-smaller CSV manifest."""
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        rows = list(reader)

    if not 1 <= len(rows) <= 8:
        raise ValueError("Manifest must contain between 1 and 8 samples")

    samples: list[Sample] = []
    for row in rows:
        try:
            sample = Sample(
                sample_id=row["sample_id"].strip(),
                source_well=row["source_well"].strip().upper(),
                plate_row=row["plate_row"].strip().upper(),
                source_volume_ul=float(row["source_volume_ul"]),
                dead_volume_ul=float(row["dead_volume_ul"]),
            )
        except (TypeError, ValueError) as error:
            raise ValueError("Volumes must be numeric") from error

        if not sample.sample_id:
            raise ValueError("Sample ID cannot be empty")
        if sample.source_well not in VALID_SOURCE_WELLS:
            raise ValueError(f"Invalid source well: {sample.source_well}")
        if sample.plate_row not in VALID_PLATE_ROWS:
            raise ValueError(f"Invalid plate row: {sample.plate_row}")
        if sample.source_volume_ul < 20 + sample.dead_volume_ul:
            raise ValueError(
                f"{sample.sample_id} has insufficient source volume"
            )
        if sample.dead_volume_ul < 0:
            raise ValueError("Dead volume cannot be negative")
        samples.append(sample)

    _require_unique(samples, "sample_id")
    _require_unique(samples, "source_well")
    _require_unique(samples, "plate_row")
    return samples


def _require_unique(samples: list[Sample], attribute: str) -> None:
    values = [getattr(sample, attribute) for sample in samples]
    if len(values) != len(set(values)):
        raise ValueError(f"Duplicate {attribute} values are not allowed")


def required_diluent_ul(sample_count: int, overage_fraction: float = 0.10) -> int:
    """Calculate diluent requirement for six wells/sample plus two controls."""
    if not 1 <= sample_count <= 8:
        raise ValueError("sample_count must be between 1 and 8")
    if overage_fraction < 0:
        raise ValueError("overage_fraction cannot be negative")
    base_volume = (sample_count * 6 + 2) * 180
    return round(base_volume * (1 + overage_fraction))


def dilution_factors(points: int = 6, step_factor: int = 10) -> list[int]:
    """Return cumulative dilution factors for a serial dilution."""
    if points < 1 or step_factor <= 1:
        raise ValueError("points must be positive and step_factor > 1")
    return [step_factor**point for point in range(1, points + 1)]
