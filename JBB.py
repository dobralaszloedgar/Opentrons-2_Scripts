from opentrons import protocol_api

metadata = {"protocolName": "Janus Bottlebrush Graft-To and PLA ROP",
            "author": "Edgar Dobra",
            "description": "This protocol is for Grafting-to after stock solutions of PS-Li and Poly-NorEO were prepared, followed by Lactide addition."
            }

requirements = {"robotType": "OT-2", "apiLevel": "2.22"}

def run(protocol: protocol_api.ProtocolContext):
    # Initializing Labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 9)
    tiprack_2 = protocol.load_labware('opentrons_96_tiprack_1000ul', protocol_api.OFF_DECK)
    tiprack_3 = protocol.load_labware('opentrons_96_tiprack_1000ul', protocol_api.OFF_DECK)
    pipette = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[tiprack, tiprack_2, tiprack_3])
    stirplate_1 = protocol.load_labware('wellplate_20ml_vial', 10)
    stirplate_2 = protocol.load_labware('wellplate_20ml_vial', 7)
    stirplate_3 = protocol.load_labware('wellplate_20ml_vial', 4)
    aliquot_well_plates = protocol.load_labware('1.5ml_gpc_vial_aluminum_block', 11)
    PS_R = protocol.load_labware('wellplate_50ml_vial', 3)
    BB_R = protocol.load_labware('wellplate_20ml_vial', 6)
    THF_r = protocol.load_labware('pyrex_reservoir_100ml', 8)
    Lac_R = protocol.load_labware('jar_200ml', 1)
    Q_R = protocol.load_labware('20ml_reservoir', 2)
    LA_R = protocol.load_labware('20ml_reservoir', 5)


    # Parameter List
    # LOCATIONS


    polymer_well_list = [stirplate_1['A1'], stirplate_1['A3'], stirplate_1['A5'], stirplate_1['A7'],
                         stirplate_1['B2'], stirplate_1['B4'], stirplate_1['B6'], stirplate_1['B8'],
                         stirplate_1['C1'],
                         stirplate_1['C3'], stirplate_1['C5'], stirplate_1['C7'], stirplate_2['A1'],
                         stirplate_2['A3'], stirplate_2['A5'], stirplate_2['A7'], stirplate_2['B2'],
                         stirplate_2['B4'],
                         stirplate_2['B6'], stirplate_2['B8'], stirplate_2['C1'], stirplate_2['C3'],
                         stirplate_2['C5'], stirplate_2['C7'], stirplate_3['A1'], stirplate_3['A3'],
                         stirplate_3['A5'],
                         stirplate_3['A7'], stirplate_3['B2'], stirplate_3['B4'], stirplate_3['B6'],
                         stirplate_3['B8'], stirplate_3['C1'], stirplate_3['C3'], stirplate_3['C5'],
                         stirplate_3['C7']
                         ]

    aliquots_well_list = [aliquot_well_plates['A1'], aliquot_well_plates['A2'], aliquot_well_plates['A3'],
                            aliquot_well_plates['A4'], aliquot_well_plates['A5'], aliquot_well_plates['A6'],
                            aliquot_well_plates['A7'], aliquot_well_plates['A8'], aliquot_well_plates['B1'],
                            aliquot_well_plates['B2'], aliquot_well_plates['B3'], aliquot_well_plates['B4'],
                            aliquot_well_plates['B5'], aliquot_well_plates['B6'], aliquot_well_plates['B7'],
                            aliquot_well_plates['B8'], aliquot_well_plates['C1'], aliquot_well_plates['C2'],
                            aliquot_well_plates['C3'], aliquot_well_plates['C4'], aliquot_well_plates['C5'],
                            aliquot_well_plates['C6'], aliquot_well_plates['C7'], aliquot_well_plates['C8'],
                            aliquot_well_plates['D1'], aliquot_well_plates['D2'], aliquot_well_plates['D3'],
                            aliquot_well_plates['D4'], aliquot_well_plates['D5'], aliquot_well_plates['D6'],
                            aliquot_well_plates['D7'], aliquot_well_plates['D8'], aliquot_well_plates['E1'],
                            aliquot_well_plates['E2'], aliquot_well_plates['E3'], aliquot_well_plates['E4']
                            ]

    PS_Li_reservoir_1 = PS_R['A1']
    PS_Li_reservoir_2 = PS_R['A3']
    PS_Li_reservoir_3 = PS_R['B2']

    BB_reservoir_1 = BB_R['A1']
    BB_reservoir_2 = BB_R['A3']
    BB_reservoir_3 = BB_R['B2']
    BB_reservoir_4 = BB_R['B4']

    Lactide_reservoir = Lac_R['A1']
    Quencher_reservoir = Q_R['A1']
    THF_reservoir = THF_r['A1']
    Livingness_Agent_reservoir = LA_R['A1']

    # VOLUMES
    PS_Li = [2514.23, 1825.69, 1179.61, 2514.23, 1825.69, 1179.61, 2514.23, 1825.69, 1179.61, 2522.32, 1829.96, 1181.39, 2522.32, 1829.96, 1181.39, 2522.32, 1829.96, 1181.39, 2524.36, 1831.03, 1181.84, 2524.36, 1831.03, 1181.84, 2524.36, 1831.03, 1181.84, 2524.70, 1831.21, 1181.91, 2524.70, 1831.21, 1181.91, 2524.70, 1831.21, 1181.91]
    BB = [992.69, 720.84, 465.75, 992.69, 720.84, 465.75, 992.69, 720.84, 465.75, 976.57, 708.50, 457.40, 976.57, 708.50, 457.40, 976.57, 708.50, 457.40, 972.52, 705.41, 455.31, 972.52, 705.41, 455.31, 972.52, 705.41, 455.31, 971.84, 704.90, 454.96, 971.84, 704.90, 454.96, 971.84, 704.90, 454.96]
    Lactide = [2262.80, 3286.25, 4246.60, 2262.80, 3286.25, 4246.60, 2262.80, 3286.25, 4246.60, 2270.09, 3293.93, 4253.01, 2270.09, 3293.93, 4253.01, 2270.09, 3293.93, 4253.01, 2271.92, 3295.85, 4254.61, 2271.92, 3295.85, 4254.61, 2271.92, 3295.85, 4254.61, 2272.23, 3296.18, 4254.88, 2272.23, 3296.18, 4254.88, 2272.23, 3296.18, 4254.88]
    Quencher = [230.28, 167.22, 108.04, 230.28, 167.22, 108.04, 230.28, 167.22, 108.04, 231.02, 167.61, 108.20, 231.02, 167.61, 108.20, 231.02, 167.61, 108.20, 231.21, 167.70, 108.24, 231.21, 167.70, 108.24, 231.21, 167.70, 108.24, 231.24, 167.72, 108.25, 231.24, 167.72, 108.25, 231.24, 167.72, 108.25]
    Livingness_Agent = [302.12, 219.38, 141.75, 302.12, 219.38, 141.75, 302.12, 219.38, 141.75, 303.09, 219.89, 141.96, 303.09, 219.89, 141.96, 303.09, 219.89, 141.96, 303.33, 220.02, 142.01, 303.33, 220.02, 142.01, 303.33, 220.02, 142.01, 303.37, 220.04, 142.02, 303.37, 220.04, 142.02, 303.37, 220.04, 142.02]


    # Define Functions
    def fill_aliquots(source, destination, volume=1000, bottom_clearance_aspirate=3, bottom_clearance_dispense=3):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.distribute([volume] * len(destination), source, destination,
                           disposal_volume=0)

    def take_aliquot(source, destination, volume=60, mix_times=2, mix_volume=200, bottom_clearance_aspirate=1, bottom_clearance_dispense=3):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume), new_tip='always')

    pipette.starting_tip = tiprack.well('A1')

    # Distribute PS-Li
    pipette.well_bottom_clearance.aspirate = 3
    pipette.well_bottom_clearance.dispense = 50
    pipette.distribute(PS_Li[0:3]+PS_Li[9:12]+PS_Li[18:21]+PS_Li[27:30], PS_Li_reservoir_1, polymer_well_list[0:3]+
                       polymer_well_list[9:12]+polymer_well_list[18:21]+polymer_well_list[27:30], disposal_volume=0)
    pipette.distribute(PS_Li[3:6]+PS_Li[12:15]+PS_Li[21:24]+PS_Li[30:33], PS_Li_reservoir_2, polymer_well_list[3:6]+
                       polymer_well_list[12:15]+polymer_well_list[21:24]+polymer_well_list[30:33], disposal_volume=0)
    pipette.distribute(PS_Li[6:9]+PS_Li[15:18]+PS_Li[24:27]+PS_Li[33:36], PS_Li_reservoir_3, polymer_well_list[6:9]+
                       polymer_well_list[15:18]+polymer_well_list[24:27]+polymer_well_list[33:36], disposal_volume=0)

    # Add BB
    pipette.well_bottom_clearance.aspirate = 2
    pipette.well_bottom_clearance.dispense = 50
    pipette.transfer(BB[0:9], BB_reservoir_1, polymer_well_list[0:9], disposal_volume=0)
    pipette.transfer(BB[9:18], BB_reservoir_2, polymer_well_list[9:18], disposal_volume=0)
    pipette.transfer(BB[18:27], BB_reservoir_3, polymer_well_list[18:27], disposal_volume=0)
    pipette.transfer(BB[27:36], BB_reservoir_4, polymer_well_list[27:36], disposal_volume=0)

    # Pause
    protocol.pause("Aliquot fill stage next")

    # Fill aliquots with THF
    fill_aliquots(source=THF_reservoir, destination=aliquots_well_list)

    # Take aliquots
    take_aliquot(source=polymer_well_list, destination=aliquots_well_list)

    # Add Livingness Agent
    pipette.well_bottom_clearance.aspirate = 2
    pipette.well_bottom_clearance.dispense = 50
    pipette.distribute(Livingness_Agent, Livingness_Agent_reservoir, polymer_well_list)


    # Pause
    protocol.move_labware(labware=tiprack, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tiprack_2, new_location=9)
    pipette.starting_tip = tiprack_2.well('A1')
    protocol.pause("Please replace pipette tips, and GPC vials, let Livingness Agent Stir")


    # Fill aliquots with THF
    fill_aliquots(source=THF_reservoir, destination=aliquots_well_list)

    # Add Lactide & Quench
    bottom_clearance = 100-30
    counter = 0
    threshold_index = 1  # will go from 1 to 10
    for i in range(len(polymer_well_list)):
        # set aspirate clearance for Lactide
        pipette.well_bottom_clearance.aspirate = bottom_clearance
        pipette.well_bottom_clearance.dispense = 50
        pipette.transfer(Lactide[i], Lactide_reservoir, polymer_well_list[i])
        counter += Lactide[i]

        while threshold_index <= 10 and counter > 10000 * threshold_index:
            bottom_clearance = max(2, bottom_clearance - 10)
            threshold_index += 1

        pipette.well_bottom_clearance.aspirate = 2
        pipette.well_bottom_clearance.dispense = 50
        pipette.transfer(Quencher[i], Quencher_reservoir, polymer_well_list[i])

    # Pause
    protocol.move_labware(labware=tiprack_2, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tiprack_3, new_location=9)
    pipette.starting_tip = tiprack_3.well('A1')
    protocol.pause("Please make sure enough THF is present for aliquots")

    # Fill aliquots with THF
    fill_aliquots(source=THF_reservoir, destination=aliquots_well_list)

    # Take aliquots
    take_aliquot(source=polymer_well_list, destination=aliquots_well_list)


