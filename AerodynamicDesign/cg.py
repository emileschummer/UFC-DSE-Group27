# Individual component masses in kg
M_landing_leg = 0.0625 
M_vertical_prop_pole = 0.812 
M_wing_box = 2.40
M_equipment = 1.88
M_batt = 11.45
M_fuselage = 1.33
M_wing_and_tail = 0.74 # Combined mass for wing and tail skin
M_vertical_prop = 0.195
M_vert_motor = 0.47
M_vert_esc = 0.074
M_push_motor = 0.61
M_push_prop = 0.07
M_pusher_esc = 0.11

# Quantities of each component
N_landing_leg = 4
N_vertical_prop_pole = 2
N_vertical_prop_systems = 4 # Includes prop, motor, and ESC
N_pusher_systems = 1 # Includes motor, prop, and ESC

# Calculate total mass
total_mass = (M_landing_leg * N_landing_leg) + \
             (M_vertical_prop_pole * N_vertical_prop_pole) + \
             M_wing_box + \
             M_equipment + \
             M_batt + \
             M_fuselage + \
             M_wing_and_tail + \
             ((M_vertical_prop + M_vert_motor + M_vert_esc) * N_vertical_prop_systems) + \
             ((M_push_motor + M_push_prop + M_pusher_esc) * N_pusher_systems)

print(f"Total UAV Mass: {total_mass:.2f} kg")