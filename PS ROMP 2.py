from opentrons import protocol_api

metadata = {'apiLevel': '2.19',
            'protocolName': 'PS ROMP 2',
            'description': '''This protocol is for running PS ROMPs.''',
            'author': 'Edgar Dobra'}


def run(protocol: protocol_api.ProtocolContext):
    # Initializing Labware.
    g3_tube_tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 10)
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 1)
    pipette = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[g3_tube_tiprack, tiprack])
    well_plates_g3 = protocol.load_labware('falcon_24_wellplate_4000ul', 7)
    well_plates = protocol.load_labware('falcon_24_wellplate_4000ul', 2)
    reservoir = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', 6)
    beaker_100ml = protocol.load_labware('beaker_100ml', 5)


    # Parameter List
    G3_tube_tip_location = 'F3'
    starting_tip_location = 'A1'
    starting_tip_location_2 = 'C1'

    G3_volume = 72
    PS_list = [1000, 2000, 1000, 2000]
    polymer_well_list = [well_plates['D1'], well_plates['D2'], well_plates['D3'], well_plates['D4']]
    allequotes_well_list = [well_plates['A1'], well_plates['A2'], well_plates['A3'], well_plates['A4']]

    G3_well = 'A1'
    PS_reservoir = 'A1'
    THF_quench_reservoir = 'A1'
    quencher = 'D6'

    # Fill allequotes with THF
    pipette.starting_tip = tiprack.well(starting_tip_location)
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.distribute([1000] * 4, beaker_100ml[THF_quench_reservoir], allequotes_well_list, disposal_volume=0)

    # Distributing the PS
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.distribute(PS_list, reservoir[PS_reservoir],
                       polymer_well_list, disposal_volume=0, blow_out=False)

    # Filling up G3
    pipette.starting_tip = g3_tube_tiprack.well(G3_tube_tip_location)
    pipette.pick_up_tip()
    pipette.move_to(well_plates_g3[G3_well].top())
    pipette.move_to(well_plates_g3[G3_well].bottom(z=10))
    protocol.pause("Load the G3")
    pipette.move_to(well_plates_g3[G3_well].top())
    pipette.return_tip()
    pipette.move_to(g3_tube_tiprack[G3_tube_tip_location].top(z=100))


    # Distribute G3
    pipette.starting_tip = tiprack.well(starting_tip_location_2)
    pipette.well_bottom_clearance.dispense = 2
    pipette.well_bottom_clearance.aspirate = 0
    pipette.transfer(G3_volume, well_plates_g3[G3_well], polymer_well_list[0], mix_after=(3, 200))
    pipette.transfer(G3_volume, well_plates_g3[G3_well], polymer_well_list[1], mix_after=(3, 200))

    protocol.delay(minutes=39)

    # Distribute G3 again
    pipette.well_bottom_clearance.dispense = 2
    pipette.well_bottom_clearance.aspirate = 0
    pipette.transfer(G3_volume, well_plates_g3[G3_well], polymer_well_list[2], mix_after=(3, 200))
    pipette.transfer(G3_volume, well_plates_g3[G3_well], polymer_well_list[3], mix_after=(3, 200))

    protocol.delay(minutes=19)

    # Aliquotes 1 60min
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(60, polymer_well_list[0], allequotes_well_list[0], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[0], mix_after=(2, 200))
    pipette.transfer(60, polymer_well_list[1], allequotes_well_list[1], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[1], mix_after=(2, 200))

    # Reaction 1 quench
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(500, well_plates_g3[quencher], polymer_well_list[0], mix_after=(3, 500))
    pipette.transfer(500, well_plates_g3[quencher], polymer_well_list[1], mix_after=(3, 500))

    protocol.delay(minutes=37)

    # Aliquotes 2 60min
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(60, polymer_well_list[2], allequotes_well_list[2], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[2], mix_after=(2, 200))
    pipette.transfer(60, polymer_well_list[3], allequotes_well_list[3], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[3], mix_after=(2, 200))

    # Reaction 2 quench
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(500, well_plates_g3[quencher], polymer_well_list[2], mix_after=(3, 500))
    pipette.transfer(500, well_plates_g3[quencher], polymer_well_list[3], mix_after=(3, 500))

