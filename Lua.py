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
    PS_Li = [2654.41, 2219.87, 1672.32, 2624.63, 2189.18, 1643.75, 2605.94, 2170.00, 1625.98, 2680.40, 2238.02, 1682.60,
             2650.76, 2207.32, 1653.96, 2632.13, 2188.13, 1636.14, 2674.04, 2233.58, 1680.09, 2644.36, 2202.89, 1651.47,
             2625.72, 2183.69, 1633.66, 2237.97, 2237.97, 1682.58, 2650.68, 2207.27, 1653.93, 2632.06, 2188.08, 1636.12]

    BB = [785.41, 656.83, 494.82, 798.08, 665.67, 499.82, 806.04, 671.20, 502.93, 749.03, 625.41, 470.20, 761.24, 633.90,
          474.98, 768.91, 639.20, 477.95, 757.94, 633.10, 476.21, 770.26, 641.67, 481.05, 778.00, 647.03, 484.05, 625.50,
          625.50, 470.27, 761.34, 633.98, 475.05, 769.01, 639.29, 478.02]

    Lactide = [880.89, 1473.36, 2219.90, 895.10, 1493.19, 2242.33, 904.03, 1505.59, 2256.28, 889.51, 1485.41, 2233.55,
               904.01, 1505.56, 2256.25, 913.11, 1518.17, 2270.38, 887.40, 1482.46, 2230.21, 901.83, 1502.54, 2252.85,
               910.89, 1515.09, 2266.93, 1485.38, 1485.38, 2233.51, 903.98, 1505.53, 2256.22, 913.09, 1518.13, 2270.34]

    Quencher = [4*x for x in [179.29, 149.94, 112.96, 182.18, 151.96, 114.10, 184.00, 153.22, 114.81, 181.05, 151.17,
                              113.65, 184.00, 153.22, 114.81, 185.85, 154.50, 115.52, 180.62, 150.87, 113.48, 183.55,
                              152.91, 114.63, 185.40, 154.19, 115.35, 151.16, 151.16, 113.65, 183.99, 153.21, 114.80,
                              185.84, 154.50, 115.52]]

    Livingness_Agent = [235.22, 196.71, 148.19, 239.02, 199.36, 149.69, 241.40, 201.02, 150.62, 237.53, 198.32, 149.10,
                        241.40, 201.01, 150.62, 243.83, 202.70, 151.56, 236.96, 197.93, 148.88, 240.81, 200.61, 150.39,
                        243.23, 202.29, 151.33, 198.32, 198.32, 149.10, 241.39, 201.01, 150.62, 243.82, 202.69, 151.56]

    # Define Functions
    def fill_aliquots(source, destination, volume=1000, bottom_clearance_aspirate=3, bottom_clearance_dispense=10):
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.distribute([volume] * len(destination), source, destination, disposal_volume=0)
        pipette.distribute([50] * len(destination), Quencher_reservoir, destination, disposal_volume=200, blow_out=True, blowout_location="source well")

    def take_aliquot(source, destination, volume=60, mix_times=1, mix_volume=200, bottom_clearance_aspirate=1, bottom_clearance_dispense=3):
        pipette.flow_rate.aspirate = 30
        pipette.well_bottom_clearance.dispense = bottom_clearance_dispense
        pipette.well_bottom_clearance.aspirate = bottom_clearance_aspirate
        pipette.transfer(volume, source, destination, mix_after=(mix_times, mix_volume), new_tip='always')
        pipette.flow_rate.aspirate = 274.7


    # Pause
    protocol.move_labware(labware=tiprack, new_location=protocol_api.OFF_DECK)
    protocol.move_labware(labware=tiprack_2, new_location=9)
    pipette.starting_tip = tiprack_2.well('A1')
    protocol.pause("Let Livingness Agent stir for 30 minutes")



    '''
    # Add Lactide & Quench with lowering pipette depth throughout
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
        pipette.well_bottom_clearance.aspirate = 1
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
