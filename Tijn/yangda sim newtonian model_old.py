import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#initial conditions
W = 200
m = W/9.81
piAe = 30
Clalpha = 4.5
Clhalpha = 4.3
Clvbeta = 4.3
stall = 0.24
stallh = 0.26
stalv = 0.3
Cl0 = 0.2
Clh0 = -0.1
b = 3
bh = 0.3
bv = 0.3
dihederal = 0.03
S = 1
Sh = 0.3
Sv = 0.1
rho = 1.2
Cd0 = 0.05
Cmac = -0.01
Vx = 30
Vy = 2
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
lh = 1
lv = 1
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
aeleron_delta = 0
Cldelta = 0.5
Clhdelta = 0.5
Clvdelta = 0.5

def get_Cx():
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Ct = np.cos(alpha)*Cd - np.sin(alpha)*Cl
    Cx = Tx/(0.5*rho*S*V**2) -np.sin(pitch)*W/(0.5*rho*S*V**2) - Ct
    return Cx

def get_Cz():
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Clh = alpha*Clhalpha*(Sh/S) + (lh*pitchrate/V)*Clhalpha*(Sh/S) + Clh0*(Sh/S) + Clhdelta*elevator_delta*(Sh/S)
    Cn = np.cos(alpha)*Cl + np.sin(alpha)*Cd
    Cnh = np.cos(alpha)*Clh
    Cz = np.cos(pitch)*np.cos(roll)*W/(0.5*rho*S*V**2) - Tz/(0.5*rho*S*V**2) - Cn - Cnh
    return Cz

def get_Cy():
    Clv = -beta*Clvbeta*(Sv/S) + (lv*yawrate/V)*Clvbeta*(Sv/S) - Clvdelta*rudder_delta*(Sv/S)  #rudder due to sidelip and yaw rotation

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

    yaw_velocity = b*yawrate/4 #due to yawrate
    Cm = 0.5*Cn*yaw_velocity/V    #roll moment needs to be figured out better
    return Cm


def get_Cmx_rollrate():
    Cm = b**2*rollrate/(V*8)*np.cos(alpha)*Clalpha/c #due to roll rate wing
    Cmh = bh**2*rollrate/(V*8)*np.cos(alpha)*Clhalpha*(Sh/S)/c#horizontal stabilizer
    Cmv = bv**2*rollrate/(V*8)*np.cos(beta)*Clvbeta*(Sv/S)/c#vertical stabilizer
    return -(Cm + Cmh + Cmv)


def get_Cmx_vertical_yawrate_and_sideslip():
    Clv = -beta*Clvbeta*(Sv/S) + (lv*yawrate/V)*Clvbeta*(Sv/S) - Clvdelta*rudder_delta*(Sv/S)  #due to sideslip on the vertical stabilizer
    Cy = np.cos(beta)*Clv
    Cmv_beta = Cy*bv/c 
    return 0*Cmv_beta


def get_Cmx(): #roll moment add roll due to vertical tail lift and due to yaw rate 
    Cmx = get_Cmx_beta() + get_Cmx_rollrate() + get_Cmx_yawrate() + get_Cmx_vertical_yawrate_and_sideslip() + diff_thrust_roll/(0.5*rho*S*c*V**2)
    return Cmx

def get_Cmz(): #yaw moment
    Clv = +beta*Clvbeta*(Sv/S) - (lv*yawrate/V)*Clvbeta*(Sv/S) + Clvdelta*rudder_delta*(Sv/S)
    Cy = np.cos(beta)*Clv
    Cmv = Cy*lv/c
    return Cmv + diff_thrust_yaw/(0.5*rho*S*c*V**2)

def get_Cmy(): #pitch moment
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Clh = alpha*Clhalpha*(Sh/S) + (lh*pitchrate/V)*Clhalpha*(Sh/S) + Clh0*(Sh/S) + Clhdelta*elevator_delta*(Sh/S)
    Cn = np.cos(alpha)*Cl + np.sin(alpha)*Cd
    Cnh = np.cos(alpha)*Clh
    Cm = Cn*l/c + Cmac
    Cmh = -Cnh*lh/c
    Cmy = diff_thrust_pitch/(0.5*rho*S*c*V**2) + Cm + Cmh
    return Cmy

t = 0
tend = 9
dt = 0.005

velocity = [V]
AoA = [alpha*180/np.pi]
sideslip = [beta*180/np.pi]
pitchangle = [pitch*180/np.pi]
yawangle = [yaw*180/np.pi]
rollangle = [roll*180/np.pi]
time = [t]
X = 0
Y = 0
Z = 0
Xlst = [X]
Ylst = [Y]
Zlst = [Z]
dist = 0
distance = [dist]


while t < tend:
    t = t +dt


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
    Y = Y + dt*(np.sin(yaw)*np.cos(pitch)*Vx - (np.cos(yaw)*np.cos(roll) + np.sin(pitch)*np.sin(yaw)*np.sin(roll))*Vy + (np.cos(yaw)*np.sin(roll) + np.sin(pitch)*np.sin(yaw)*np.cos(roll))*Vz)
    Z = Z + dt*(np.sin(pitch)*Vx - np.cos(pitch)*np.sin(roll)*Vy - np.cos(pitch)*np.cos(roll)*Vz)
    dist = dist + ((dt*np.sin(yaw-beta)*V*np.cos(pitch))**2+(dt*np.cos(yaw-beta)*V*np.cos(pitch))**2)**0.5
    
    
    p = p + dt*Mx/Ix #roll
    q = q + dt*My/Iy #pitch
    r = r + dt*Mz/Iz #yaw

    rollrate = p + q * np.sin(roll)  + r * np.cos(roll) * np.tan(pitch)
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
    beta = np.arcsin(Vy/V) # dit ben ik niet helemaal zeker van
    velocity.append(V)
    AoA.append(alpha*180/np.pi)
    sideslip.append(beta*180/np.pi)
    pitchangle.append(pitch*180/np.pi)
    yawangle.append(yaw*180/np.pi)
    rollangle.append(roll*180/np.pi)
    time.append(t)
    Xlst.append(X)
    Ylst.append(Y)
    Zlst.append(Z)
    distance.append(dist)
plot_mode = 1
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

if plot_mode == 0:

    ax1.plot(time, velocity)
    ax1.set_title("velocity")

    ax1.grid(True)

    ax2.plot(time, AoA)
    ax2.set_title("AoA")

    ax2.grid(True)

    ax3.plot(time, pitchangle)
    ax3.set_title("pitch")
    ax3.set_xlabel("Time [s]")

else:
    ax1.plot(time, sideslip)
    ax1.set_title("sideslip")

    ax1.grid(True)

    ax2.plot(time, yawangle)
    ax2.set_title("yaw")

    ax2.grid(True)

    ax3.plot(time, rollangle)
    ax3.set_title("roll")
    ax3.set_xlabel("Time [s]")
ax3.grid(True)
plt.show()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # removed sharex=True

ax1.plot(Xlst, Ylst)
ax1.set_title("X/Y coordinates")
ax1.grid(True)
ax1.set_aspect('equal', adjustable='box')
ax2.plot(distance, Zlst)
ax2.set_title("Altitude")
ax2.grid(True)

plt.tight_layout()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Test data
ax.plot(Xlst, Ylst, Zlst, label='Trajectory')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Plot Test')
ax.legend()
plt.show()



