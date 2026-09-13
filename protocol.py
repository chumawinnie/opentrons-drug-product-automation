"""Simulated OT-2 drug-product sample preparation protocol.

Educational use only. Simulator-tested; not validated on physical hardware.
"""

from opentrons import protocol_api

metadata = {
    "protocolName": "Drug Product Sample Preparation and Serial Dilution",
    "author": "Chukwuma Winner Obiora",
    "description": "Eight-sample, six-point 1:10 serial dilution with controls",
    "apiLevel": "2.22",
}

SAMPLE_IDS = [f"DP-{index:03d}" for index in range(1, 9)]
DILUENT_VOLUME_UL = 180
TRANSFER_VOLUME_UL = 20
MIX_VOLUME_UL = 100
MIX_REPETITIONS = 3


def add_parameters(parameters: protocol_api.Parameters) -> None:
    """Expose safe run-time parameters in the Opentrons App."""
    parameters.add_int(
        variable_name="sample_count",
        display_name="Number of samples",
        description="Number of drug-product samples to process",
        default=8,
        minimum=1,
        maximum=8,
    )


def run(protocol: protocol_api.ProtocolContext) -> None:
    """Prepare an eight-row serial-dilution plate."""
    sample_count = getattr(protocol.params, "sample_count", 8)

    plate = protocol.load_labware(
        "corning_96_wellplate_360ul_flat", "1", "Dilution plate"
    )
    reservoir = protocol.load_labware(
        "nest_12_reservoir_15ml", "2", "Diluent and waste"
    )
    sample_rack = protocol.load_labware(
        "opentrons_24_tuberack_nest_1.5ml_snapcap", "3", "Sample tubes"
    )
    tiprack_1 = protocol.load_labware("opentrons_96_tiprack_300ul", "4")
    tiprack_2 = protocol.load_labware("opentrons_96_tiprack_300ul", "7")
    pipette = protocol.load_instrument(
        "p300_single_gen2", "right", tip_racks=[tiprack_1, tiprack_2]
    )

    diluent = reservoir["A1"]
    liquid_waste = reservoir["A12"]
    source_well_names = ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2"]
    source_wells = [sample_rack[name] for name in source_well_names[:sample_count]]
    destination_rows = plate.rows()[:sample_count]

    protocol.comment(
        f"Preparing {sample_count} samples: {', '.join(SAMPLE_IDS[:sample_count])}"
    )

    # Dispense diluent without contacting destination liquid.
    pipette.pick_up_tip()
    for row in destination_rows:
        for destination in row[:6]:
            pipette.aspirate(DILUENT_VOLUME_UL, diluent.bottom(2))
            pipette.dispense(DILUENT_VOLUME_UL, destination.top(-2))
    pipette.drop_tip()

    # Add sample to column 1, then perform 1:10 serial dilutions.
    for sample_id, source, row in zip(
        SAMPLE_IDS[:sample_count], source_wells, destination_rows, strict=True
    ):
        protocol.comment(f"Processing {sample_id}")

        pipette.pick_up_tip()
        pipette.aspirate(TRANSFER_VOLUME_UL, source.bottom(1))
        pipette.dispense(TRANSFER_VOLUME_UL, row[0].bottom(2))
        pipette.mix(MIX_REPETITIONS, MIX_VOLUME_UL, row[0])
        pipette.drop_tip()

        for column_index in range(5):
            pipette.pick_up_tip()
            pipette.mix(MIX_REPETITIONS, MIX_VOLUME_UL, row[column_index])
            pipette.aspirate(TRANSFER_VOLUME_UL, row[column_index].bottom(2))
            pipette.dispense(
                TRANSFER_VOLUME_UL, row[column_index + 1].bottom(2)
            )
            pipette.drop_tip()

        # Normalize the final well to the same final volume as the other wells.
        pipette.pick_up_tip()
        pipette.mix(MIX_REPETITIONS, MIX_VOLUME_UL, row[5])
        pipette.aspirate(TRANSFER_VOLUME_UL, row[5].bottom(2))
        pipette.dispense(TRANSFER_VOLUME_UL, liquid_waste.top(-2))
        pipette.drop_tip()

    # Demonstration controls, separate from the dilution series.
    positive_control = plate["G12"]
    blank_control = plate["H12"]

    pipette.pick_up_tip()
    pipette.aspirate(DILUENT_VOLUME_UL, diluent.bottom(2))
    pipette.dispense(DILUENT_VOLUME_UL, positive_control.top(-2))
    pipette.aspirate(DILUENT_VOLUME_UL, diluent.bottom(2))
    pipette.dispense(DILUENT_VOLUME_UL, blank_control.top(-2))
    pipette.drop_tip()

    protocol.comment("Protocol complete. Review run log and plate map.")
