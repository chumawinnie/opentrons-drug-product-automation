# Simulated Drug-Product Sample Preparation

Python-based liquid-handling protocol for an **Opentrons OT-2**. The project
models a drug-product sample preparation workflow in which eight samples are
transferred to a 96-well plate and diluted across six concentrations.

> This is an educational, in-silico automation project. It has been tested with
> the Opentrons simulator but has not been executed on physical hardware or
> validated for clinical, diagnostic, or GxP use.

## What the workflow demonstrates

- Automated diluent dispensing and sample transfer
- Six-point 1:10 serial dilution for eight samples
- Fresh-tip strategy to reduce cross-contamination risk
- Configurable sample manifest with input validation
- Positive control and blank allocation
- Pre-run volume calculations
- Opentrons API simulation
- Unit tests, risk assessment, and a prospective validation plan

## Deck layout

| Slot | Labware | Purpose |
| --- | --- | --- |
| 1 | 96-well flat-bottom plate | Dilution series |
| 2 | 12-channel reservoir | Diluent and liquid waste |
| 3 | 24-position tube rack | Drug-product samples |
| 4, 7 | 300 uL tip racks | Pipette tips |

Samples DP-001 to DP-008 occupy rows A to H. Columns 1 to 6 contain the
successive dilution points. Wells G12 and H12 are reserved for a positive
control and blank.

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
python -m scripts.validate_manifest sample_manifest.csv
python -m opentrons.simulate protocol.py > simulation_output/simulation.txt
```

## Design assumptions

- Each dilution well starts with 180 uL diluent.
- A 20 uL transfer produces a 1:10 dilution.
- Each dilution step mixes three times with 100 uL before transferring.
- A final 20 uL is removed from column 6 so all assay wells end at 180 uL.
- Source tubes must contain at least the required volume plus configured
  dead volume.

See [workflow documentation](docs/workflow.md),
[validation plan](docs/validation_plan.md), and
[risk assessment](docs/risk_assessment.md).

## Honest portfolio description

Developed and simulator-tested a Python/Opentrons protocol for automated
drug-product sample preparation and serial dilution. Implemented configurable
sample inputs, volume validation, contamination-aware tip handling, controls,
unit tests, risk assessment, and technical documentation.

## Licence

MIT. Opentrons is a trademark of its respective owner. 
