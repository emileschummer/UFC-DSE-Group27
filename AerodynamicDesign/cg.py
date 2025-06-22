M_landing_leg = 0.0625 #four
M_vertical_prop_pole = 0.812 #2
M_wing_box = 2.40
M_skin = 2.06
M_equipment = 3.75
M_batt = 11.45
M_fuselage = 1.33
M_wing_and_tail = 1.74
M_vertical_prop = 0.195
M_vert_motor = 0.47
M_vert_esc = 0.074
M_push_motor = 0.61
M_push_prop = 0.07
M_pusher_esc = 0.11


S_wing = 2.32
S_tail = 0.23
S_vert = 0.0224

M_wing_skin = S_wing/(S_wing+S_tail+S_vert)*M_wing_and_tail
M_tail_skin = (S_tail+S_vert)/(S_wing+S_tail+S_vert)*M_wing_and_tail

l_vertical_prop_pole = 2.29 
d_prop = 0.74
MAC = 0.736
l_aft_props = 1.653
l_quart_wing_from_prop = 0.996
l_pusher_prop_from_quart_chord = 0.774258
egg_mid = 0.20
l_batt = 0.35
l_fus_tip = 0.87525
L_quartWingToquartTail = 1.5333

cg = ((d_prop/2+l_vertical_prop_pole/2)*2*M_vertical_prop_pole + d_prop/2 * (M_landing_leg+M_vert_motor+M_vert_esc+M_vertical_prop) * 2 + (l_aft_props + d_prop/2)*(M_landing_leg+M_vert_motor+M_vert_esc+M_vertical_prop)*2 + (M_wing_box+M_wing_skin)*(l_quart_wing_from_prop + d_prop/2) + (M_push_motor+M_push_prop+M_pusher_esc)*(l_pusher_prop_from_quart_chord+d_prop/2)+(M_equipment+M_batt+M_fuselage)*(l_batt+l_fus_tip)+(L_quartWingToquartTail+l_quart_wing_from_prop+d_prop/2)*M_tail_skin)/(2*M_vertical_prop_pole+(M_landing_leg+M_vert_motor+M_vert_esc+M_vertical_prop) * 2+(M_landing_leg+M_vert_motor+M_vert_esc+M_vertical_prop)*2+(M_wing_box+M_wing_skin)+(M_push_motor+M_push_prop+M_pusher_esc)+(M_equipment+M_batt+M_fuselage)+M_tail_skin)
print(cg)