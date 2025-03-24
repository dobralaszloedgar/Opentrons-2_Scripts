from opentrons import protocol_api

metadata = {'apiLevel': '2.19',
            'protocolName': 'G3 Experiment',
            'description': '''This protocol is for running PS polymerization experiments to test G3 degradation.''',
            'author': 'Edgar Dobra'}


def run(protocol: protocol_api.ProtocolContext):
    # Initializing Labware.
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 10)
    pipette = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[tiprack])
    well_plates = protocol.load_labware('falcon_24_wellplate_4000ul', 2)
    reservoir = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', 4)
    beaker_100ml = protocol.load_labware('beaker_100ml', 6)


    # Parameter List
    puncture_tip_location = 'A1'  # <--- Parameter
    PS_pipette_tip_location = 'B1'  # <--- Parameter
    G3_pipette_tip_location = 'C1'

    G3_well = 'D6'
    PS_reservoir = 'A1'
    THF_reservoir = 'A1'
    puncture_tip_bottom_offset = -10  # <--- Parameter
    gpc_top_offset = 10  # <--- Parameter
    bottom_offset = 6  # <--- Parameter
    vial_pullout = 35  # <--- Parameter

    # Distributing the PS
    pipette.well_bottom_clearance.dispense = 5
    pipette.well_bottom_clearance.aspirate = 3
    pipette.starting_tip = tiprack.well(PS_pipette_tip_location)
    pipette.distribute([640, 640, 640, 640, 640, 640, 640], reservoir[PS_reservoir],
                       [well_plates['A1'], well_plates['A2'], well_plates['A3'], well_plates['A4'], well_plates['A5'],
                        well_plates['A6'], well_plates['B1']], blow_out=True, blowout_location='source well')

    # Puncturing a parafilm covered vial then pulling out
    pipette.pick_up_tip(tiprack[puncture_tip_location])
    pipette.move_to(well_plates[G3_well].top(z=vial_pullout))
    pipette.move_to(well_plates[G3_well].bottom(z=0))
    protocol.delay(seconds=2)
    pipette.move_to(well_plates[G3_well].top(z=vial_pullout))
    pipette.drop_tip()

    # Distribute G3
    pipette.starting_tip = tiprack.well(G3_pipette_tip_location)
    pipette.well_bottom_clearance.dispense = 5
    pipette.well_bottom_clearance.aspirate = 3
    protocol.delay(seconds=10)
    pipette.transfer(92, well_plates[G3_well], well_plates["A1"], mix_after=(3, 200))
    protocol.delay(minutes=3)
    pipette.transfer(92, well_plates[G3_well], well_plates["A2"], mix_after=(3, 200))
    protocol.delay(minutes=3)
    pipette.transfer(92, well_plates[G3_well], well_plates["A3"], mix_after=(3, 200))
    protocol.delay(minutes=4)
    pipette.transfer(92, well_plates[G3_well], well_plates["A4"], mix_after=(3, 200))
    protocol.delay(minutes=5)
    pipette.transfer(92, well_plates[G3_well], well_plates["A5"], mix_after=(3, 200))
    protocol.delay(minutes=15)
    pipette.transfer(92, well_plates[G3_well], well_plates["A6"], mix_after=(3, 200))
    protocol.delay(minutes=20)
    pipette.transfer(92, well_plates[G3_well], well_plates["B1"], mix_after=(3, 200))

    # Distributing the THF
    pipette.well_bottom_clearance.dispense = 5
    pipette.well_bottom_clearance.aspirate = 3
    pipette.distribute([1000, 1000, 1000, 1000, 1000, 1000, 1000], beaker_100ml[THF_reservoir],
                       [well_plates['C1'], well_plates['C2'], well_plates['C3'], well_plates['C4'], well_plates['C5'],
                        well_plates['C6'], well_plates['D1']], disposal_volume=0)

    protocol.delay(minutes=30)
    pipette.transfer(60, well_plates["A1"], well_plates["C1"])
    pipette.transfer(60, well_plates["A2"], well_plates["C2"])
    pipette.transfer(60, well_plates["A3"], well_plates["C3"])
    pipette.transfer(60, well_plates["A4"], well_plates["C4"])
    pipette.transfer(60, well_plates["A5"], well_plates["C5"])
    pipette.transfer(60, well_plates["A6"], well_plates["C6"])
    pipette.transfer(60, well_plates["B1"], well_plates["D1"])

