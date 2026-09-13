import csv

import pytest

from src.planning import dilution_factors, load_manifest, required_diluent_ul


def write_manifest(tmp_path, rows):
    path = tmp_path / "manifest.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "sample_id",
                "source_well",
                "plate_row",
                "source_volume_ul",
                "dead_volume_ul",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    return path


def valid_row(**overrides):
    row = {
        "sample_id": "DP-001",
        "source_well": "A1",
        "plate_row": "A",
        "source_volume_ul": "100",
        "dead_volume_ul": "20",
    }
    row.update(overrides)
    return row


def test_valid_manifest(tmp_path):
    samples = load_manifest(write_manifest(tmp_path, [valid_row()]))
    assert samples[0].sample_id == "DP-001"


def test_duplicate_destination_row_rejected(tmp_path):
    rows = [
        valid_row(),
        valid_row(sample_id="DP-002", source_well="A2"),
    ]
    with pytest.raises(ValueError, match="Duplicate plate_row"):
        load_manifest(write_manifest(tmp_path, rows))


def test_insufficient_volume_rejected(tmp_path):
    with pytest.raises(ValueError, match="insufficient"):
        load_manifest(
            write_manifest(
                tmp_path,
                [valid_row(source_volume_ul="35", dead_volume_ul="20")],
            )
        )


def test_diluent_volume_includes_controls_and_overage():
    assert required_diluent_ul(8) == 9900


def test_six_point_tenfold_dilution():
    assert dilution_factors() == [10, 100, 1000, 10000, 100000, 1000000]
