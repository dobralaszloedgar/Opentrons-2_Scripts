from opentrons import protocol_api

metadata = {'apiLevel': '2.22',
            'protocolName': 'New PS-b-PLA ROMP-RAFT With Stirring',
            'description': '''This protocol is for running PS-b-PLA ROMPs.''',
            'author': 'Edgar Dobra'}


def run(protocol: protocol_api.ProtocolContext):
    # Initializing Labware.
    g3_tube_tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 10)
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 1)
    pipette = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[g3_tube_tiprack, tiprack])
    well_plates_g3 = protocol.load_labware('falcon_24_wellplate_4000ul', 7)
    well_plates = protocol.load_labware('falcon_24_wellplate_4000ul', 5)
    reservoir = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', 6)
    beaker_100ml = protocol.load_labware('beaker_100ml', 8)

    # Parameter List
    G3_tube_tip_location = 'F3'
    starting_tip_location = 'A1'
    starting_tip_location_2 = 'D1'

    G3_volume = 72
    PS_list = [500]
    Norbonene_list = [50]
    DBU_list = [469.4]
    Lactide_list = [773.5]
    polymer_well_list = [well_plates['D1']]
    allequotes_well_list = [well_plates['A1'], well_plates['A2'], well_plates['A3']]

    G3_reservoir = well_plates_g3['A1']
    quencher = well_plates['D6']
    boric_acid = well_plates['C6']

    PS_reservoir = well_plates['C1']
    Norbonene_reservoir = well_plates['C2']
    Lactide_reservoir = well_plates['C3']
    DBU_reservoir = well_plates['C4']

    THF_quench_reservoir = well_plates['A6']


    # Fill allequotes with THF
    pipette.starting_tip = tiprack.well(starting_tip_location)
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.distribute([1000] * len(allequotes_well_list), THF_quench_reservoir, allequotes_well_list,
                       disposal_volume=0)

    '''
    # Distributing the PS
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 1
    pipette.distribute(PS_list, PS_reservoir, polymer_well_list, blow_out=True,
                       blowout_location="source well")
    '''

    # Filling up G3
    pipette.starting_tip = g3_tube_tiprack.well(G3_tube_tip_location)
    pipette.pick_up_tip()
    pipette.move_to(G3_reservoir.top())
    pipette.move_to(G3_reservoir.bottom(z=10))
    protocol.pause("Load the G3")
    pipette.move_to(G3_reservoir.top())
    pipette.return_tip()
    pipette.move_to(g3_tube_tiprack[G3_tube_tip_location].top(z=100))

    # Distribute G3
    pipette.starting_tip = tiprack.well(starting_tip_location_2)
    pipette.well_bottom_clearance.dispense = 5
    pipette.well_bottom_clearance.aspirate = 0
    pipette.transfer(G3_volume, G3_reservoir, polymer_well_list[0])

    protocol.delay(minutes=30)

    # Aliquot and add Norbonene
    pipette.well_bottom_clearance.dispense = 5
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(60, polymer_well_list[0], allequotes_well_list[0], mix_after=(2, 200))
    pipette.transfer(60, quencher, allequotes_well_list[0], mix_after=(2, 200))
    pipette.transfer(Norbonene_list[0], Norbonene_reservoir, polymer_well_list[0])

    protocol.delay(minutes=20)

    # Quench with DVE and aliquot
    pipette.well_bottom_clearance.dispense = 5
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(60, quencher, polymer_well_list[0])
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(60, polymer_well_list[0], allequotes_well_list[1], mix_after=(2, 200))
    pipette.transfer(60, quencher, allequotes_well_list[1], mix_after=(2, 200))

    # Add Lactide + DBU
    pipette.well_bottom_clearance.dispense = 5
    pipette.well_bottom_clearance.aspirate = 1
    pipette.transfer(Lactide_list[0], Lactide_reservoir, polymer_well_list)
    pipette.transfer(DBU_list[0], DBU_reservoir, polymer_well_list)

    protocol.delay(minutes=60)

    # Quench with Boric Acid and aliquot
    pipette.well_bottom_clearance.dispense = 5
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(300, boric_acid, polymer_well_list[0])
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.transfer(60, polymer_well_list[0], allequotes_well_list[2], mix_after=(2, 200))


