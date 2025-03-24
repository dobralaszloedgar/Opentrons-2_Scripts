from opentrons import protocol_api

metadata = {'apiLevel': '2.19',
            'protocolName': 'PS-b-PLA ROMP',
            'description': '''This protocol is for running PS-b-PLA ROMPs.''',
            'author': 'Edgar Dobra'}


def run(protocol: protocol_api.ProtocolContext):
    # Initializing Labware
    g3_tube_tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 10)                                      # "Name of labware", location on the deck of OT-2
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 1)
    pipette = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[g3_tube_tiprack, tiprack])        # The pipette load, only change tip_racks and specify the accessible tip racks to the machine
    well_plates_g3 = protocol.load_labware('falcon_24_wellplate_4000ul', 7)
    well_plates = protocol.load_labware('falcon_24_wellplate_4000ul', 2)
    reservoir = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', 6)
    beaker_100ml = protocol.load_labware('beaker_100ml', 5)

    # Parameter List (just some parameters for later reaction)

    # Locations
    G3_tube_tip_location = 'F3'     # Locations are always a list, first--letter specifies row, second--number specifies column
    starting_tip_location = 'A1'
    starting_tip_location_2 = 'C1'
    G3_well = 'A1'
    PS_reservoir = 'A1'
    PLA_reservoir = 'A2'
    THF_quench_reservoir = 'A1'
    quencher = 'D6'                 # Well lists can also be specified as seen below
    polymer_well_list = [well_plates['D1'], well_plates['D2'], well_plates['D3'], well_plates['D4']]
    allequotes_well_list = [well_plates['A1'], well_plates['A2'], well_plates['A3'], well_plates['A4'],
                            well_plates['A5'], well_plates['A6'], well_plates['B1'], well_plates['B2']]

    # Volumes
    G3_volume = 36              # Volume can be a number, or a list
    PS_list = [475, 375, 312.5, 250]
    PLA_list = [54, 270, 405, 540]

    # Fill aliquots with THF
    pipette.starting_tip = tiprack.well(starting_tip_location)      # Starting tip needs to be specified
    pipette.well_bottom_clearance.dispense = 3                      # Bottom clearance for aspiration and dispensation, default set to 2 mm, counted from bottom of well, not wellplate
    pipette.well_bottom_clearance.aspirate = 3                      # Distribute command can distribute amount of liquid (list) from one reservoir into a list of wells
    pipette.distribute([1000] * len(allequotes_well_list), beaker_100ml[THF_quench_reservoir], allequotes_well_list, disposal_volume=0)     # If disposal volume is not zero, it will dispose some liquid for more precise measurement, if you want to change it look at the API documentation

    # Distributing the PS
    pipette.well_bottom_clearance.dispense = 3
    pipette.well_bottom_clearance.aspirate = 3
    pipette.distribute(PS_list, reservoir[PS_reservoir], polymer_well_list, blow_out=True, blowout_location="source well")  # Disposes small amount of liquid with last two parameters into source well, for more precise measurements, opposite of previous

    # Filling up G3
    pipette.starting_tip = g3_tube_tiprack.well(G3_tube_tip_location)       # Specify new starting tip for pipette with micro-floating tube
    pipette.pick_up_tip()                                                   # Pick up tip, not needed at distribute or transfer
    pipette.move_to(well_plates_g3[G3_well].top())                          # Move to the top of the well plate, top offset = 0 mm
    pipette.move_to(well_plates_g3[G3_well].bottom(z=10))                   # Move to the bottom of the well plate, bottom offset = 10 mm
    protocol.pause("Load the G3")                                           # Pauses until manual resume from prompt
    pipette.move_to(well_plates_g3[G3_well].top())
    pipette.return_tip()                                                    # Returns the tip to where it picked it up, only needed where pick_up_tip was called
    pipette.move_to(g3_tube_tiprack[G3_tube_tip_location].top(z=100))       # Important step not to popp out the microfloating tip, if not used it will dislodge the tiprack and potentially explode the tip

    # Distribute G3
    pipette.starting_tip = tiprack.well(starting_tip_location_2)            # New starting tip specified
    pipette.well_bottom_clearance.dispense = 2
    pipette.well_bottom_clearance.aspirate = 0
    pipette.transfer(G3_volume, well_plates_g3[G3_well], polymer_well_list[0], mix_after=(3, 200))      # Transfers liquid amount from one container to another, with mixing after transfer (3x 200uL)
    pipette.transfer(G3_volume, well_plates_g3[G3_well], polymer_well_list[1], mix_after=(3, 200))
    pipette.transfer(G3_volume, well_plates_g3[G3_well], polymer_well_list[2], mix_after=(3, 200))
    pipette.transfer(G3_volume, well_plates_g3[G3_well], polymer_well_list[3], mix_after=(3, 200))

    protocol.delay(minutes=15)          # Delays protocol, seconds, minutes can be specified

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

    protocol.delay(minutes=20)

    # Final aliquots
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
