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
    THF_r = protocol.load_labware('100ml_beaker_2', 8)       #change depending on what I use
    Lac_R = protocol.load_labware('pyrex_reservoir_100ml', 1)
    Q_R = protocol.load_labware('20ml_reservoir', 2)
    LA_R = protocol.load_labware('20ml_reservoir', 5)

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
    PS_Li = [2661.82, 2225.04, 1675.26, 2632.07, 2194.36, 1646.67, 2613.40, 2175.17, 1628.88, 2670.74, 2231.28, 1678.79,
             2641.04, 2200.59, 1650.17, 2622.39, 2181.39, 1632.37, 2672.98, 2232.84, 1679.68, 2643.30, 2202.15, 1651.05,
             2624.65, 2182.96, 1633.25, 2233.10, 2233.10, 1679.82, 2643.67, 2202.41, 1651.20, 2625.03, 2183.22, 1633.40]
    BB = [775.05, 647.87, 487.79, 787.59, 656.61, 492.73, 795.46, 662.07, 495.80, 762.56, 637.08, 479.33,
            774.94, 645.70, 484.20, 782.71, 651.09, 487.22, 759.42, 634.37, 477.21, 771.76, 642.96, 482.06,
            779.51, 648.33, 485.07, 633.92, 633.92, 476.86, 771.23, 642.50, 481.70, 778.98, 647.87, 484.71]
    Lactide = [883.35, 1476.80, 2223.80, 897.64, 1496.72, 2246.31, 906.61, 1509.17, 2260.31, 886.31, 1480.93, 2228.48,
                900.70, 1500.97, 2251.09, 909.73, 1513.49, 2265.15, 887.05, 1481.97, 2229.66, 901.46, 1502.03, 2252.29,
                910.52, 1514.58, 2266.36, 1482.15, 1482.15, 2229.85, 901.59, 1502.21, 2252.49, 910.65, 1514.76, 2266.56]
    Quencher = [179.79, 150.29, 113.15, 182.70, 152.32, 114.30, 184.53, 153.58, 115.01, 180.39, 150.71, 113.39,
                183.32, 152.75, 114.54, 185.16, 154.02, 115.26, 180.54, 150.82, 113.45, 183.48, 152.86, 114.60,
                185.32, 154.13, 115.32, 150.83, 150.83, 113.46, 183.50, 152.88, 114.61, 185.35, 154.15, 115.33]
    Livingness_Agent = [235.88, 197.17, 148.45, 239.69, 199.83, 149.96, 242.09, 201.50, 150.89, 236.67, 197.73, 148.77,
                        240.51, 200.40, 150.28, 242.92, 202.07, 151.21, 236.87, 197.86, 148.85, 240.72, 200.54, 150.36,
                        243.13, 202.22, 151.30, 197.89, 197.89, 148.86, 240.75, 200.57, 150.37, 243.17, 202.24, 151.31]

    # Define Functions
    def fill_aliquots(source, destination, volume=1000, bottom_clearance_aspirate=3, bottom_clearance_dispense=10):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.distribute([volume] * len(destination), source, destination, disposal_volume=0)
        pipette.distribute([50] * len(destination), Quencher_reservoir, destination, disposal_volume=0)

    def take_aliquot(source, destination, volume=60, mix_times=2, mix_volume=200, bottom_clearance_aspirate=1, bottom_clearance_dispense=3):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume), new_tip='always')

    # Run starts here
    pipette.starting_tip = tiprack.well('A1')

    # Distribute PS-Li
    pipette.well_bottom_clearance.aspirate = 1
    pipette.well_bottom_clearance.dispense = 50
    pipette.distribute(PS_Li[0:3]+PS_Li[9:12]+PS_Li[18:21]+PS_Li[27:30], PS_Li_reservoir_1, polymer_well_list[0:3]+
                       polymer_well_list[9:12]+polymer_well_list[18:21]+polymer_well_list[27:30], disposal_volume=0)
    pipette.distribute(PS_Li[3:6]+PS_Li[12:15]+PS_Li[21:24]+PS_Li[30:33], PS_Li_reservoir_2, polymer_well_list[3:6]+
                       polymer_well_list[12:15]+polymer_well_list[21:24]+polymer_well_list[30:33], disposal_volume=0)
    pipette.distribute(PS_Li[6:9]+PS_Li[15:18]+PS_Li[24:27]+PS_Li[33:36], PS_Li_reservoir_3, polymer_well_list[6:9]+
                       polymer_well_list[15:18]+polymer_well_list[24:27]+polymer_well_list[33:36], disposal_volume=0)

    # Add BB
    pipette.well_bottom_clearance.aspirate = 1
    pipette.well_bottom_clearance.dispense = 50
    pipette.transfer(BB[0:9], BB_reservoir_1, polymer_well_list[0:9], disposal_volume=0)
    pipette.transfer(BB[9:18], BB_reservoir_2, polymer_well_list[9:18], disposal_volume=0)
    pipette.transfer(BB[18:27], BB_reservoir_3, polymer_well_list[18:27], disposal_volume=0)
    pipette.transfer(BB[27:36], BB_reservoir_4, polymer_well_list[27:36], disposal_volume=0)

    # Pause
    protocol.pause("Aliquot fill stage and Livingness Agent addition next, WAIT 60 minutes")

    # Fill aliquots with THF
    fill_aliquots(source=THF_reservoir, destination=aliquots_well_list)

    # Take aliquots
    take_aliquot(source=polymer_well_list, destination=aliquots_well_list)

    # Add Livingness Agent
    pipette.well_bottom_clearance.aspirate = 1
    pipette.well_bottom_clearance.dispense = 50
    pipette.distribute(Livingness_Agent, Livingness_Agent_reservoir, polymer_well_list, disposal_volume=0) #Check if any gets split into 2


    # Pause
    protocol.move_labware(labware=tiprack, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tiprack_2, new_location=9)
    pipette.starting_tip = tiprack_2.well('A1')
    protocol.pause("Let Livingness Agent stir for 30 minutes")



    '''
    # Add Lactide & Quench V1
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
    '''

    # Add Lactide & Quench V2
    pipette.well_bottom_clearance.dispense = 50
    for i in range(len(polymer_well_list)):
        pipette.well_bottom_clearance.aspirate = 2
        pipette.transfer(Lactide[i], Lactide_reservoir, polymer_well_list[i])
        # protocol.delay(seconds=30)
        pipette.well_bottom_clearance.aspirate = 2
        pipette.transfer(Quencher[i], Quencher_reservoir, polymer_well_list[i])

    # Pause
    protocol.move_labware(labware=tiprack_2, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tiprack_3, new_location=9)
    pipette.starting_tip = tiprack_3.well('A1')
    protocol.pause("Please make sure enough THF is present for aliquots, GPC vials are ready, and replace tiprack")

    # Fill aliquots with THF
    fill_aliquots(source=THF_reservoir, destination=aliquots_well_list)

    # Take aliquots
    take_aliquot(source=polymer_well_list, destination=aliquots_well_list)
