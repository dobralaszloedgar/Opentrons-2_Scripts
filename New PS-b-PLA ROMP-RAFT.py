from opentrons import protocol_api

metadata = {'apiLevel': '2.21',
            'protocolName': 'New PS-b-2PLA ROMP-RAFT ',
            'description': '''This protocol is for running PS-b-2PLA ROMP-RAFT.''',
            'author': 'Edgar Dobra'}


def run(protocol: protocol_api.ProtocolContext):
    # Initializing Labware.
    g3_tube_tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 10)
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 1)
    pipette = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[g3_tube_tiprack, tiprack])
    well_plates_g3 = protocol.load_labware('falcon_24_wellplate_4000ul', 7)
    well_plates = protocol.load_labware('falcon_24_wellplate_hotplate_4000ul', 2)
    well_plates_2 = protocol.load_labware('falcon_24_wellplate_4000ul', 9)
    aliquot_well_plates = protocol.load_labware('1.5ml_gpc_vial_aluminum_block', 6)
    beaker_100ml = protocol.load_labware('pyrex_reservoir_100ml', 5)

    # Parameter List
    G3_tube_tip_location = g3_tube_tiprack.well('F3')
    starting_tip_location = tiprack.well('A1')
    starting_tip_location_2 = tiprack.well('B1')
    starting_tip_location_3 = tiprack.well('C1')

    G3_volume = 72
    PS_list = [500]
    Norbonene_list = [50]
    DBU_list = [469.4]
    Lactide_list = [773.5]
    polymer_well_list = [well_plates['B3']]
    linear_PLA_well_list = [well_plates['D2']]
    aliquots_well_list_1 = [aliquot_well_plates['A1'], aliquot_well_plates['A2'], aliquot_well_plates['A3']]
    aliquots_well_list_2 = [aliquot_well_plates['A4'], aliquot_well_plates['A5'], aliquot_well_plates['A6'], aliquot_well_plates['B1'], aliquot_well_plates['B2'], aliquot_well_plates['B3']]
    aliquots_well_list_3 = [aliquot_well_plates['C1'], aliquot_well_plates['C2'], aliquot_well_plates['C3'], aliquot_well_plates['C4'], aliquot_well_plates['C5'], aliquot_well_plates['C6'], aliquot_well_plates['D1'], aliquot_well_plates['D2'], aliquot_well_plates['D3']]


    G3_reservoir = well_plates_g3['A1']
    quencher = well_plates_2['A6']
    boric_acid = well_plates_2['A4']

    Norbonene_reservoir = well_plates_2['A1']
    Lactide_reservoir = well_plates_2['A2']
    DBU_reservoir = well_plates_2['A3']

    THF_quench_reservoir = beaker_100ml['A1']
    #THF_reservoir = beaker_100ml['A1']

    aliquot_times = [5, 10, 15, 30, 60, 2*60, 3*60, 6*60, 12*60]  # in minutes after start

    # Define Functions
    def fill_aliquots(source, destination, volume=1000, bottom_clearance_aspirate=3, bottom_clearance_dispense=3, starting_tip=starting_tip_location):
        pipette.starting_tip = starting_tip
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.distribute([volume] * len(destination), source, destination,
                           disposal_volume=0)

    def fill_G3(reservoir=G3_reservoir, starting_tip=G3_tube_tip_location):
        pipette.starting_tip = starting_tip
        pipette.pick_up_tip()
        pipette.move_to(reservoir.top())
        pipette.move_to(reservoir.bottom(z=10))
        protocol.pause("Load the G3")
        pipette.move_to(reservoir.top())
        pipette.return_tip()
        pipette.move_to(starting_tip.top(z=100))

    def distribute_G3(source, destination, volume=G3_volume, mix_times=3, mix_volume=200, bottom_clearance_aspirate=1, bottom_clearance_dispense=2, starting_tip=starting_tip_location_3):
        pipette.starting_tip = starting_tip
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume))

    def take_aliquot(source, destination, volume=60, mix_times=2, mix_volume=200, bottom_clearance_aspirate=1, bottom_clearance_dispense=3):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume))

    def quench(source, destination, volume=60, mix_times=2, mix_volume=200, bottom_clearance_aspirate=1, bottom_clearance_dispense=3):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume))

    def add_Norbonene(source, destination, volume, mix_times=4, mix_volume=500, bottom_clearance_aspirate=1, bottom_clearance_dispense=3):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume))

    def add_Lactide(source, destination, volume, mix_times=4, mix_volume=500, bottom_clearance_aspirate=3, bottom_clearance_dispense=3):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume))

    def add_DBU(source, destination, volume, mix_times=4, mix_volume=500, bottom_clearance_aspirate=1, bottom_clearance_dispense=3):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume))

    # Fill allequotes with THF
    fill_aliquots(source=THF_quench_reservoir, destination=aliquots_well_list_1, starting_tip=starting_tip_location)
   # fill_aliquots(source=THF_reservoir, destination=aliquots_well_list_2+aliquots_well_list_3, starting_tip=starting_tip_location_2)

    '''
    # Distributing the PS
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 1
    pipette.distribute(PS_list, PS_reservoir, polymer_well_list, blow_out=True,
                       blowout_location="source well")
    '''

    # Filling up G3
    fill_G3()

    # Distribute G3
    distribute_G3(G3_reservoir, polymer_well_list[0], G3_volume)
    protocol.delay(minutes=10)

    # Aliquot and add Norbonene
    take_aliquot(polymer_well_list[0], aliquots_well_list_1[0], 60)
    quench(quencher, aliquots_well_list_1[0], 60)
    add_Norbonene(Norbonene_reservoir, polymer_well_list[0], Norbonene_list[0])
    protocol.delay(minutes=10)

    # Quench with DVE and aliquot
    quench(quencher, polymer_well_list[0], 100, 4, 500)
    take_aliquot(polymer_well_list[0], aliquots_well_list_1[1])

    # Add Lactide + DBU
    add_Lactide(Lactide_reservoir, polymer_well_list, Lactide_list[0])
    add_DBU(DBU_reservoir, polymer_well_list, DBU_list[0])

    '''
    # Start Linear PLA
    pipette.transfer(600, THF_reservoir, linear_PLA_well_list[0])
    add_Norbonene(Norbonene_reservoir, linear_PLA_well_list[0], Norbonene_list[0])
    add_Lactide(Lactide_reservoir, linear_PLA_well_list[0], Lactide_list[0])
    add_DBU(DBU_reservoir, linear_PLA_well_list[0], DBU_list[0])
    '''
    # aliquots
    '''
    ti = 0
    for i in range(len(aliquot_times)):
        protocol.delay(minutes=aliquot_times[i]-ti)
        take_aliquot(polymer_well_list[0], aliquots_well_list_2[i])
        quench(boric_acid, aliquots_well_list_2[i], volume=100)
        take_aliquot(linear_PLA_well_list[0], aliquots_well_list_3[i], volume=100)
        quench(boric_acid, aliquots_well_list_3[i])
        ti = aliquot_times[i]
    '''
    protocol.delay(minutes=30)
    quench(boric_acid, polymer_well_list[0], volume=1000)
    protocol.delay(minutes=1)
    take_aliquot(polymer_well_list[0], aliquots_well_list_1[2])


'''
    # 5min
    take_aliquot(polymer_well_list[0], aliquots_well_list_2[0])
    quench(boric_acid, aliquots_well_list_2[0])
    take_aliquot(linear_PLA_well_list[0], aliquots_well_list_3[0])
    quench(boric_acid, aliquots_well_list_3[0])
    protocol.delay(minutes=5)

    # 10min
    take_aliquot(polymer_well_list[0], aliquots_well_list_2[1])
    quench(boric_acid, aliquots_well_list_2[1])
    take_aliquot(linear_PLA_well_list[0], aliquots_well_list_3[1])
    quench(boric_acid, aliquots_well_list_3[1])
    protocol.delay(minutes=5)

    # 15min
    take_aliquot(polymer_well_list[0], aliquots_well_list_2[2])
    quench(boric_acid, aliquots_well_list_2[2])
    take_aliquot(linear_PLA_well_list[0], aliquots_well_list_3[2])
    quench(boric_acid, aliquots_well_list_3[2])
    protocol.delay(minutes=15)

    # 30min
    take_aliquot(polymer_well_list[0], aliquots_well_list_2[3])
    quench(boric_acid, aliquots_well_list_2[3])
    take_aliquot(linear_PLA_well_list[0], aliquots_well_list_3[3])
    quench(boric_acid, aliquots_well_list_3[3])
    protocol.delay(minutes=30)

    # 1h
    take_aliquot(polymer_well_list[0], aliquots_well_list_2[4])
    quench(boric_acid, aliquots_well_list_2[4])
    take_aliquot(linear_PLA_well_list[0], aliquots_well_list_3[4])
    quench(boric_acid, aliquots_well_list_3[4])
    protocol.delay(minutes=60)

    # 2h
    take_aliquot(polymer_well_list[0], aliquots_well_list_2[5])
    quench(boric_acid, aliquots_well_list_2[5])
    take_aliquot(linear_PLA_well_list[0], aliquots_well_list_3[5])
    quench(boric_acid, aliquots_well_list_3[5])
    protocol.delay(minutes=60)

    # 3h
    take_aliquot(polymer_well_list[0], aliquots_well_list_2[6])
    quench(boric_acid, aliquots_well_list_2[6])
    take_aliquot(linear_PLA_well_list[0], aliquots_well_list_3[6])
    quench(boric_acid, aliquots_well_list_3[6])
    protocol.delay(minutes=3*60)

    # 6h
    take_aliquot(polymer_well_list[0], aliquots_well_list_2[7])
    quench(boric_acid, aliquots_well_list_2[7])
    take_aliquot(linear_PLA_well_list[0], aliquots_well_list_3[7])
    quench(boric_acid, aliquots_well_list_3[7])
    protocol.delay(minutes=6*60)

    # 12h
    take_aliquot(polymer_well_list[0], aliquots_well_list_2[8])
    quench(boric_acid, aliquots_well_list_2[8])
    take_aliquot(linear_PLA_well_list[0], aliquots_well_list_3[8])
    quench(boric_acid, aliquots_well_list_3[8])
'''
