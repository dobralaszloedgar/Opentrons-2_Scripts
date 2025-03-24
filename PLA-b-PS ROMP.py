from opentrons import protocol_api

metadata = {'apiLevel': '2.20',
            'protocolName': 'PLA-b-PS ROMP',
            'description': '''This protocol is for running PLA-b-PS ROMP.''',
            'author': 'Edgar Dobra'}


def run(protocol: protocol_api.ProtocolContext):
    # Initializing Labware.
    g3_tube_tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 10)
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 1)
    pipette = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[g3_tube_tiprack, tiprack])
    well_plates_g3 = protocol.load_labware('falcon_24_wellplate_4000ul', 7)
    well_plates = protocol.load_labware('falcon_24_wellplate_4000ul', 2)
    aliquot_well_plates = protocol.load_labware('falcon_24_wellplate_4000ul', 3)
    beaker_100ml = protocol.load_labware('pyrex_reservoir_100ml', 5)

    # Parameter List
    G3_tube_tip_location = g3_tube_tiprack.well('F3')
    starting_tip_location = tiprack.well('A1')
    starting_tip_location_2 = tiprack.well('B1')
    starting_tip_location_3 = tiprack.well('B1')


    G3_volume = 72
    PS_list = [500]
    polymer_well_list = [well_plates['D1']]
    PLA_well_list = [well_plates['D2']]
    aliquots_well_list_1 = [well_plates['A1']]
    aliquots_well_list_2 = [aliquot_well_plates['A1'], aliquot_well_plates['A2'], aliquot_well_plates['A3'], aliquot_well_plates['A4'], aliquot_well_plates['A5']]
    aliquots_well_list_3 = [aliquot_well_plates['C1'], aliquot_well_plates['C2'], aliquot_well_plates['C3'], aliquot_well_plates['C4'], aliquot_well_plates['C5'], aliquot_well_plates['C6'], aliquot_well_plates['D1'], aliquot_well_plates['D2']]


    G3_reservoir = well_plates_g3['A1']
    quencher = well_plates['D6']

    PS_reservoir = well_plates['C3']

    THF_quench_reservoir = beaker_100ml['A1']

    aliquot_times = [3, 5, 10, 15, 30]  # in minutes after start
    aliquot_times_2 = [5, 10, 15, 30, 60, 2*60, 3*60, 6*60]  # in minutes after start

    # Define Functions
    def fill_aliquots(source, destination, volume=1000, bottom_clearance_aspirate=3, bottom_clearance_dispense=3, starting_tip=starting_tip_location):
        pipette.starting_tip = starting_tip
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.distribute([volume] * len(destination), source, destination, disposal_volume=0)

    def fill_G3(reservoir=G3_reservoir, starting_tip=G3_tube_tip_location):
        pipette.starting_tip = starting_tip
        pipette.pick_up_tip()
        pipette.move_to(reservoir.top())
        pipette.move_to(reservoir.bottom(z=10))
        protocol.pause("Load the G3")
        pipette.move_to(reservoir.top())
        pipette.return_tip()
        pipette.move_to(starting_tip.top(z=100))

    def distribute_G3(source, destination, volume=G3_volume, mix_times=3, mix_volume=200, bottom_clearance_aspirate=1, bottom_clearance_dispense=2, starting_tip=starting_tip_location_2):
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

    def add_PS(source, destination, volume, mix_times=4, mix_volume=500, bottom_clearance_aspirate=3, bottom_clearance_dispense=3):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume))


    # Fill allequotes with THF
    fill_aliquots(source=THF_quench_reservoir, destination=aliquots_well_list_1+aliquots_well_list_2+aliquots_well_list_3, starting_tip=starting_tip_location)

    # Filling up G3
    fill_G3()

    # Distribute G3
    distribute_G3(G3_reservoir, PLA_well_list[0], G3_volume, starting_tip=starting_tip_location_2)
    distribute_G3(G3_reservoir, polymer_well_list[0], G3_volume, starting_tip=starting_tip_location_3)

    # Aliquots for PLA ROMP
    ti = 0
    for i in range(len(aliquot_times)):
        protocol.delay(minutes=aliquot_times[i] - ti)
        take_aliquot(PLA_well_list[0], aliquots_well_list_2[i])
        quench(quencher, aliquots_well_list_2[i], volume=60)
        ti = aliquot_times[i]

    # Aliquot and add PS
    take_aliquot(polymer_well_list[0], aliquots_well_list_1[0], 60)
    add_PS(PS_reservoir, polymer_well_list[0], PS_list[0])

    ti = 0
    for i in range(len(aliquot_times_2)):
        protocol.delay(minutes=aliquot_times_2[i] - ti)
        take_aliquot(polymer_well_list[0], aliquots_well_list_3[i])
        quench(quencher, aliquots_well_list_3[i], volume=60)
        ti = aliquot_times_2[i]

    # Quench with DVE
    quench(quencher, polymer_well_list[0], 500, 4, 500)

