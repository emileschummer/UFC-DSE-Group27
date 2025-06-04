import pygame
import numpy as np
import sys
import time

# --- Initialize Pygame ---
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1300, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flight Simulator - Thrust Control")
background = pygame.transform.scale(pygame.image.load("tour_belgie.png"), screen.get_size())
ship = pygame.image.load('blueship.png').convert_alpha()
original_size = ship.get_size()
scale_factor = 0.07
scaled_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
ship = pygame.transform.smoothscale(ship, scaled_size)
max_dim = max(scaled_size)
square_surf = pygame.Surface((max_dim, max_dim), pygame.SRCALPHA)
ship_rect = ship.get_rect(center=(max_dim // 2, max_dim // 2))
square_surf.blit(ship, ship_rect)
#compas



# Pre-generate all rotated images
rotated_images = [pygame.transform.rotate(square_surf, angle) for angle in range(360)]



# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clock setup
clock = pygame.time.Clock()

# --- Flight Sim Initial Conditions ---
stall = 22*np.pi/180
W = 200
m = W/9.81
piAe = 30
Clalpha = 4.635
Clhalpha = 6
Clvbeta = 8
Clmax = 2.2
CLmaxh = 1.8
CLmaxv = 1.8
Cl0 = 0.934
Clh0 = 0.6
b = 3
bh = 0.3
bv = 0.3
dihederal = 0
S = 1
Sh = 0.2
Sv = 0.2
rho = 1.2
Cd0 = 0.05
Cmac = -0.5
Vx = 45
Vy = 0
Vz = 0
V = (Vx**2 + Vy**2 + Vz**2)**0.5
alpha = np.sin(Vz/V)
beta = np.sin(Vy/V)
pitch = 0
yaw = 0
roll = 0
pitchrate = 0
yawrate = 0
rollrate = 0
p = 0
q = 0
r = 0
lh = 3
lv = 3
l = 0
c = 0.36
Ix = 1.5
Iy = 12
Iz = 12
Cmalpha = 0
Tz = 0
Tx = 0
diff_thrust_pitch = 0
diff_thrust_roll = 0
diff_thrust_yaw = 0
elevator_delta = 0
rudder_delta = 0
aeleron_delta = 0.05
Cldelta = 0.5
Clhdelta = 0.5
Clvdelta = 0.5
X = 100
Y = 300
Z = 300
dt = 0.01

# --- Aerodynamic Functions (from user code) ---
def get_Cx():
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Ct = np.cos(alpha)*Cd - np.sin(alpha)*Cl
    Cx = Tx/(0.5*rho*S*V**2) -np.sin(pitch)*W/(0.5*rho*S*V**2) - Ct
    return Cx

def get_Cz():
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Clh = np.arcsin((lh*q + Vz)/V)*Clhalpha*(Sh/S) + Clh0*(Sh/S) + Clhdelta*elevator_delta*(Sh/S)
    Cn = np.cos(alpha)*Cl + np.sin(alpha)*Cd
    Cnh = np.cos(alpha)*Clh
    Cz = np.cos(pitch)*np.cos(roll)*W/(0.5*rho*S*V**2) - Tz/(0.5*rho*S*V**2) - Cn - Cnh
    return Cz

def get_Cy():
    Clv =  np.arcsin((-Vy + lv*r)/V)*Clvbeta*(Sv/S) - Clvdelta*rudder_delta*(Sv/S)  #rudder due to sidelip and yaw rotation

    Cy = np.cos(beta)*Clv + np.sin(roll)*np.cos(pitch)*W/(0.5*rho*S*V**2)

    return Cy

def get_Cmx_beta(): #due to dihederal and aelerons
    aeleron_moment = (b/2)*Cldelta*aeleron_delta
    dalpha = -2*Vy*np.sin(dihederal)
    dCl = dalpha*Clalpha
    
    Cm = dCl*(b/4) + aeleron_moment

    return Cm

def get_Cmx_yawrate():
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Cn = np.cos(alpha)*Cl + np.sin(alpha)*Cd

    yaw_velocity = b*r/4 #due to yawrate
    Cm = 0.5*Cn*yaw_velocity/V    #roll moment needs to be figured out better

    return Cm


def get_Cmx_rollrate():
    Cm = (b/4)*np.arcsin(b*p/(4*V))*2*Clalpha/c #due to roll rate wing
    Cmh = (bh/4)*np.arcsin(bh*p/(4*V))*2*Clhalpha*(Sh/S)/c#horizontal stabilizer
    Cmv = (bv/2)*np.arcsin(bv*p/(2*V))*Clvbeta*(Sv/S)/c#vertical stabilizer

    return -(Cm + Cmh + Cmv)


def get_Cmx_vertical_yawrate_and_sideslip():
    Clv = np.arcsin((-Vy + r*lv)/V)*Clvbeta*(Sv/S) - Clvdelta*rudder_delta*(Sv/S)  #due to sideslip on the vertical stabilizer
    Cy = np.cos(beta)*Clv
    Cmv_beta = Cy*(0.5*bv)/c

    return Cmv_beta


def get_Cmx(): #roll moment add roll due to vertical tail lift and due to yaw rate 
    Cmx = get_Cmx_beta() + get_Cmx_rollrate() + get_Cmx_yawrate() + get_Cmx_vertical_yawrate_and_sideslip() + diff_thrust_roll/(0.5*rho*S*c*V**2)
    return Cmx

def get_Cmz(): #yaw moment
    Clv = np.arcsin((-Vy-lv*r)/V)*Clvbeta*(Sv/S) + Clvdelta*rudder_delta*(Sv/S) #intersting minus situaltion
    Cy = np.cos(beta)*Clv
    Cmv = Cy*lv/c
    return Cmv + diff_thrust_yaw/(0.5*rho*S*c*V**2)

def get_Cmy(): #pitch moment
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Clh = ((Vz+lh*q)/V)*Clhalpha*(Sh/S) + Clh0*(Sh/S) + Clhdelta*elevator_delta*(Sh/S)
    Cn = np.cos(alpha)*Cl + np.sin(alpha)*Cd
    Cnh = np.cos(alpha)*Clh
    Cm = Cn*l/c + Cmac
    Cmh = -Cnh*lh/c
    Cmy = diff_thrust_pitch/(0.5*rho*S*c*V**2) + Cm + Cmh
    return Cmy


# --- Main Loop ---
running = True
trajectory = []
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Input ---

    keys = pygame.key.get_pressed()
    diff_thrust_pitch = 0
    diff_thrust_roll = 0
    diff_thrust_yaw = 0
    elevator_delta = 0
    rudder_delta = 0
    aeleron_delta = 0
    if keys[pygame.K_s]: diff_thrust_pitch += 100
    if keys[pygame.K_w]: diff_thrust_pitch -= 100
    if keys[pygame.K_d]: diff_thrust_roll += 50
    if keys[pygame.K_a]: diff_thrust_roll -= 50
    if keys[pygame.K_e]: diff_thrust_yaw += 1
    if keys[pygame.K_q]: diff_thrust_yaw -= 1
    if keys[pygame.K_UP]: elevator_delta += 0.5
    if keys[pygame.K_DOWN]: elevator_delta -= 0.5
    if keys[pygame.K_RIGHT]: aeleron_delta += 0.05
    if keys[pygame.K_LEFT]: aeleron_delta -= 0.05
    if keys[pygame.K_PERIOD]: rudder_delta += 0.5
    if keys[pygame.K_COMMA]: rudder_delta -= 0.5



    # --- Physics ---
    Fx = 0.5*rho*S*V**2 * get_Cx()
    Fy = 0.5*rho*S*V**2 * get_Cy()
    Fz = 0.5*rho*S*V**2 * get_Cz()
    Mx = 0.5*rho*S*c*V**2 * get_Cmx()
    My = 0.5*rho*S*c*V**2 * get_Cmy()
    Mz = 0.5*rho*S*c*V**2 * get_Cmz()
    Vx = Vx + dt*Fx/m
    Vy = Vy + dt*Fy/m
    Vz = Vz + dt*Fz/m
    X = X + dt*(np.cos(yaw)*np.cos(pitch)*Vx + (np.sin(yaw)*np.cos(roll) + np.sin(pitch)*np.cos(yaw)*np.sin(roll))*Vy - (np.sin(yaw)*np.sin(roll) + np.sin(pitch)*np.cos(yaw)*np.cos(roll))*Vz)
    Y = Y - dt*(np.sin(yaw)*np.cos(pitch)*Vx - (np.cos(yaw)*np.cos(roll) + np.sin(pitch)*np.sin(yaw)*np.sin(roll))*Vy + (np.cos(yaw)*np.sin(roll) + np.sin(pitch)*np.sin(yaw)*np.cos(roll))*Vz)
    Z = Z + dt*(np.sin(pitch)*Vx - np.cos(pitch)*np.sin(roll)*Vy - np.cos(pitch)*np.cos(roll)*Vz)
    
    
    
    p = p + dt*Mx/Ix #roll
    q = q + dt*My/Iy #pitch
    r = r + dt*Mz/Iz #yaw
    t0 = time.time()
    rollrate = p + q * np.sin(roll) * np.tan(pitch) + r * np.cos(roll) * np.tan(pitch)
    pitchrate = q * np.cos(roll) - r * np.sin(roll)
    yawrate = q * np.sin(roll) / np.cos(pitch) + r * np.cos(roll) / np.cos(pitch)
    roll += dt * rollrate
    pitch += dt * pitchrate
    yaw += dt * yawrate



    roll = roll + dt*rollrate
    if roll > np.pi:
        roll  = roll - 2*np.pi
    elif roll < -np.pi:
        roll = roll + 2*np.pi


    if pitch > np.pi:
        pitch  = pitch - 2*np.pi
    elif pitch < -np.pi:
        pitch = pitch + 2*np.pi


    if yaw > np.pi:
        yaw  = yaw - 2*np.pi
    elif yaw < -np.pi:
        yaw = yaw + 2*np.pi

    V = (Vx**2 + Vy**2 + Vz**2)**0.5
    alpha = np.arcsin(Vz/V)
    beta = np.arcsin(Vy/V)
    trajectory.append([int(X), int(Y)])

    # --- Drawing ---
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    # Draw trajectory
    for pos in trajectory[-500000:]:
        pygame.draw.circle(screen, (0,200,0), pos, 2)
    font = pygame.font.Font(None, 36)
    altitude_text = font.render('Altitude:' + str(int(Z)), True, (255, 255, 255))
    altitude_rect = altitude_text.get_rect(center=(WIDTH*0.9, HEIGHT*0.9))
    screen.blit(altitude_text, altitude_rect)
    if abs(alpha) > stall or abs(beta) > stall:
        stall_text = font.render('STALL!!!!!!', True, (255, 255, 255))
        stall_rect = altitude_text.get_rect(center=(WIDTH*0.5, HEIGHT*0.5))
        screen.blit(stall_text, stall_rect)


    # Draw aircraft

    pos = (int(X), int(Y))
    current_image = rotated_images[int(yaw*180/np.pi)]
    current_rect = current_image.get_rect(center=pos)

    # Draw the rotated ship
    screen.blit(current_image, current_rect)

    pygame.display.set_caption(f"pitch: {np.degrees(pitch):.1f}°  roll: {np.degrees(roll):.1f}° yaw: {np.degrees(yaw):.1f}° V: {V:.2f} Angle of Attack: {np.degrees(alpha):.1f}° sideslip: {np.degrees(beta):.1f}°")
    block_size = (50, 25)
    block_surf = pygame.Surface(block_size, pygame.SRCALPHA)
    red = (255, 0, 0)
    pygame.draw.rect(block_surf, red, (0, 0, *block_size))



    block_sky = pygame.Rect(100, 150, 50, 50)
    pygame.draw.rect(screen, (0,0,230), block_sky)
    rotated_surf = pygame.transform.rotate(block_surf, -int(roll*180/np.pi))
    rotated_rect = rotated_surf.get_rect(center=(125,200 + np.sin(pitch)*50))
    screen.blit(rotated_surf, rotated_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()