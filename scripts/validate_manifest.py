"""Validate a sample manifest and print a pre-run summary."""

from __future__ import annotations

import argparse

from src.planning import dilution_factors, load_manifest, required_diluent_ul


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="Path to sample_manifest.csv")
    args = parser.parse_args()

    samples = load_manifest(args.manifest)
    print(f"Manifest valid: {len(samples)} samples")
    print(f"Diluent required with 10% overage: {required_diluent_ul(len(samples))} uL")
    print(f"Dilution factors: {dilution_factors()}")


if __name__ == "__main__":
    main()
