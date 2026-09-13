# Workflow and plate map

## Process

1. Validate the sample manifest and calculate required volumes.
2. Load labware, samples, diluent, waste reservoir, and tips.
3. Dispense 180 uL diluent into columns 1 to 6 for every active sample row.
4. Add 20 uL sample to column 1 and mix.
5. Transfer 20 uL sequentially through columns 2 to 6, mixing before transfer.
6. Remove 20 uL from column 6 to normalize final well volumes.
7. Prepare positive-control and blank wells.
8. Review the simulation or instrument run log.

## Plate map

| Row | Columns 1-6 | Column 12 |
| --- | --- | --- |
| A | DP-001 dilution series | - |
| B | DP-002 dilution series | - |
| C | DP-003 dilution series | - |
| D | DP-004 dilution series | - |
| E | DP-005 dilution series | - |
| F | DP-006 dilution series | - |
| G | DP-007 dilution series | Positive control |
| H | DP-008 dilution series | Blank |

## Carryover controls

- A fresh tip is used for every sample addition.
- A fresh tip is used for every serial-transfer step.
- Diluent is dispensed from above the destination liquid.
- Liquid waste is isolated in reservoir channel 12.

These controls are design choices only. Their effectiveness requires physical
verification using appropriate analytical methods.
