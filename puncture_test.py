from opentrons import protocol_api
import math

metadata = {'apiLevel': '2.19',
            'protocolName': 'Flow System Aliquots',
            'description': '''This protocol is for testing to
                           determine if the Opentrons can
                           puncture a parafilm covered vial.''',
            'author': 'Michael Taleff'}

def run(protocol: protocol_api.ProtocolContext):
    # Initializing Labware.
    tiprack_location = 9 # <--- Parameter
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul',
                                    tiprack_location)
    pipette = protocol.load_instrument('p1000_single_gen2',
                                     'left', tip_racks=[tiprack])
    well_plate_location = 2 # <--- Parameter
    well_plates = protocol.load_labware('falcon_24_wellplate_1000ul',
                                        well_plate_location)

    # Parameter List
    starting_tip_location = 'A1' # <--- Parameter
    well = 'A1'
    wait_time = 2 # <--- Parameter
    top_offset = -10 # <--- Parameter
    gpc_top_offset = 10 # <--- Parameter
    bottom_offset = 6 # <--- Parameter
    vial_pullout = 35 # <--- Parameter
    
    # Puncturing a parafilm covered vial then pulling out
    pipette.starting_tip = tiprack.well(starting_tip_location)
    pipette.pick_up_tip()    
    pipette.move_to(well_plates[well].top(z=vial_pullout))
    pipette.move_to(well_plates[well].top(z=bottom_offset))
    protocol.delay(seconds=wait_time)
    pipette.move_to(well_plates[well].top(z=vial_pullout))
    pipette.drop_tip()
    
