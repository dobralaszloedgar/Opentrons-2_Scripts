from opentrons import protocol_api

metadata = {'apiLevel': '2.19',
            'protocolName': 'PS-b-PLA ROMP Small Scale',
            'description': '''This protocol is for running PS-b-PLA ROMPs.''',
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
    starting_tip_location_2 = 'D1'

    G3_volume = 36
    PS_list = [475/2, 375/2, 312.5/2, 250/2]
    PLA_list = [54/2, 270/2, 405/2, 540/2]
    polymer_well_list = [well_plates['D1'], well_plates['D2'], well_plates['D3'], well_plates['D4']]
    allequotes_well_list = [well_plates['A1'], well_plates['A2'], well_plates['A3'], well_plates['A4'], well_plates['A5'],
                            well_plates['A6'], well_plates['B1'], well_plates['B2'], well_plates['B3']]

    G3_well = 'A1'
    PS_reservoir = 'A1'
    PLA_reservoir = 'A2'
    THF_quench_reservoir = 'A1'
    quencher = 'D6'

    # Fill allequotes with THF
    pipette.starting_tip = tiprack.well(starting_tip_location)
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.distribute([1000] * len(allequotes_well_list), beaker_100ml[THF_quench_reservoir], allequotes_well_list, disposal_volume=0)

    # Distributing the PS
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.distribute(PS_list, reservoir[PS_reservoir], polymer_well_list, blow_out=True, blowout_location="source well")
    
    # Distribute the PLA for control reaction
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(540/2, reservoir[PLA_reservoir], well_plates["D5"], blow_out=True, blowout_location="source well")

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
    pipette.transfer(G3_volume, well_plates_g3[G3_well], polymer_well_list[2], mix_after=(3, 200))
    pipette.transfer(G3_volume, well_plates_g3[G3_well], polymer_well_list[3], mix_after=(3, 200))
    pipette.transfer(G3_volume, well_plates_g3[G3_well], well_plates["D5"], mix_after=(3, 200))

    protocol.delay(minutes=15)

    # Aliquot and add PLA to no. 4
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 1
    pipette.transfer(60, polymer_well_list[3], allequotes_well_list[3], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[3], mix_after=(2, 200))
    pipette.transfer(PLA_list[3], reservoir[PLA_reservoir], polymer_well_list[3], mix_after=(3, 200))

    protocol.delay(minutes=3)

    # Aliquot and add PLA to no. 3
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 1
    pipette.transfer(60, polymer_well_list[2], allequotes_well_list[2], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[2], mix_after=(2, 200))
    pipette.transfer(PLA_list[2], reservoir[PLA_reservoir], polymer_well_list[2], mix_after=(3, 200))

    protocol.delay(minutes=3)

    # Aliquot and add PLA to no. 2
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 1
    pipette.transfer(60, polymer_well_list[1], allequotes_well_list[1], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[1], mix_after=(2, 200))
    pipette.transfer(PLA_list[1], reservoir[PLA_reservoir], polymer_well_list[1], mix_after=(3, 200))

    protocol.delay(minutes=3)

    # Aliquot and add PLA to no. 1
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 1
    pipette.transfer(60, polymer_well_list[0], allequotes_well_list[0], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[0], mix_after=(2, 200))
    pipette.transfer(PLA_list[0], reservoir[PLA_reservoir], polymer_well_list[0], mix_after=(3, 200))
    
    # Quench PLA and aliquot
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(500, well_plates_g3[quencher], well_plates["D5"], mix_after=(3, 500))

    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 1
    pipette.transfer(60, well_plates["D5"], allequotes_well_list[8], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[8], mix_after=(2, 200))
    
    protocol.delay(minutes=20)

    # Final quench and aliquots
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(500, well_plates_g3[quencher], polymer_well_list[0], mix_after=(3, 500))
    pipette.transfer(500, well_plates_g3[quencher], polymer_well_list[1], mix_after=(3, 500))
    pipette.transfer(500, well_plates_g3[quencher], polymer_well_list[2], mix_after=(3, 500))
    pipette.transfer(500, well_plates_g3[quencher], polymer_well_list[3], mix_after=(3, 500))

    protocol.delay(minutes=5)

    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 1
    pipette.transfer(60, polymer_well_list[0], allequotes_well_list[4], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[4], mix_after=(2, 200))
    pipette.transfer(60, polymer_well_list[1], allequotes_well_list[5], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[5], mix_after=(2, 200))
    pipette.transfer(60, polymer_well_list[2], allequotes_well_list[6], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[6], mix_after=(2, 200))
    pipette.transfer(60, polymer_well_list[3], allequotes_well_list[7], mix_after=(2, 200))
    pipette.transfer(60, well_plates_g3[quencher], allequotes_well_list[7], mix_after=(2, 200))
