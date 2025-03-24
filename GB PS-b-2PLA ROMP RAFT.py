from opentrons import protocol_api

metadata = {
    "protocolName": "GB PS-b-2PLA ROMP RAFT",
    "author": "Edgar Dobra",
    "description": "PS-b-2PLA ROMP RAFT in GB",
}

requirements = {"robotType": "OT-2", "apiLevel": "2.22"}


def run(protocol: protocol_api.ProtocolContext):
    # Initializing Labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 9)
    pipette = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[tiprack])
    block1 = protocol.load_labware('0_stirplate_block', 1)
    block2 = protocol.load_labware('0_stirplate_block', 7)
    well_plates_stir = protocol.load_labware('4ml_wellplate_stirplate', 4)
    well_plates_normal = protocol.load_labware('falcon_24_wellplate_4000ul', 2)
    aliquot_well_plates = protocol.load_labware('1.5ml_gpc_vial_aluminum_block', 6)
    reservoir_20ml = protocol.load_labware('20ml_reservoir', 5)

    # Parameter List
    starting_tip_location = tiprack.well('D2')

    G3_volume = 72
    PS_list = [500]
    Norbonene_list = [71.73]
    DBU_list = [196.33]
    Lactide_list = [1000]
    polymer_well_list = [well_plates_stir['A1']]
    aliquots_well_list_1 = [aliquot_well_plates['A1'], aliquot_well_plates['A2'], aliquot_well_plates['A3']]

    G3_reservoir = well_plates_normal['A1']
    quencher = well_plates_normal['A6']
    boric_acid = well_plates_normal['D6']

    Norbonene_reservoir = well_plates_normal['C4']
    Lactide_reservoir = well_plates_normal['B5']
    DBU_reservoir = well_plates_normal['B6']
    THF_reservoir = reservoir_20ml['A1']

    # aliquot_times = [5, 10, 15, 30, 60, 2*60, 3*60, 6*60, 12*60]  # in minutes after start

    # Define Functions
    def fill_aliquots(source, destination, volume=1000, bottom_clearance_aspirate=3, bottom_clearance_dispense=3, starting_tip=starting_tip_location):
        pipette.starting_tip = starting_tip
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.distribute([volume] * len(destination), source, destination,
                           disposal_volume=0)

    def distribute_G3(source, destination, volume=G3_volume, bottom_clearance_aspirate=1, bottom_clearance_dispense=5):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination)

    def take_aliquot(source, destination, volume=60, mix_times=2, mix_volume=200, bottom_clearance_aspirate=1, bottom_clearance_dispense=3):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume))

    def quench(source, destination, volume=60, mix_times=2, mix_volume=200, bottom_clearance_aspirate=1, bottom_clearance_dispense=3):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume))

    def add_Norbonene(source, destination, volume, bottom_clearance_aspirate=1, bottom_clearance_dispense=5):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination)

    def add_Lactide(source, destination, volume, bottom_clearance_aspirate=3, bottom_clearance_dispense=5):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination)

    def add_DBU(source, destination, volume, bottom_clearance_aspirate=1, bottom_clearance_dispense=5):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination)

    # Fill allequotes with THF
    fill_aliquots(source=THF_reservoir, destination=aliquots_well_list_1, starting_tip=starting_tip_location)

    '''
    # Distributing the PS
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 1
    pipette.distribute(PS_list, PS_reservoir, polymer_well_list, blow_out=True,
                       blowout_location="source well")
    '''


    # Distribute G3
    distribute_G3(G3_reservoir, polymer_well_list[0], G3_volume)
    protocol.delay(minutes=15)

    # Aliquot and add Norbonene
    take_aliquot(polymer_well_list[0], aliquots_well_list_1[0], 60)
    quench(quencher, aliquots_well_list_1[0], 60)
    add_Norbonene(Norbonene_reservoir, polymer_well_list[0], Norbonene_list[0])
    protocol.delay(minutes=30)

    # Quench with DVE and aliquot
    quench(quencher, polymer_well_list[0], 160, mix_times=0)
    take_aliquot(polymer_well_list[0], aliquots_well_list_1[1])

    # Add Lactide + DBU
    add_DBU(DBU_reservoir, polymer_well_list, DBU_list[0])
    add_Lactide(Lactide_reservoir, polymer_well_list, Lactide_list[0])
    protocol.delay(minutes=60)

    quench(boric_acid, polymer_well_list[0], 1000, mix_times=0)
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
