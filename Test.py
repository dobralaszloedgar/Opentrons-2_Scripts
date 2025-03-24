from opentrons import protocol_api

metadata = {
    "protocolName": "Testing",
    "author": "Edgar Dobra",
    "description": "PS-b-2PLA ROMP RAFT in GB",
}

requirements = {"robotType": "OT-2", "apiLevel": "2.22"}


def run(protocol: protocol_api.ProtocolContext):
    # Initializing Labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 9)
    pipette = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[tiprack])
    reservoir_20ml = protocol.load_labware('20ml_reservoir', 5)

    pipette.pick_up_tip()
    pipette.move_to(reservoir_20ml["A1"].top())



