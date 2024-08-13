from std_atm import *
import numpy as np
import matplotlib.pyplot as plt


def altitude_mission_altitude(t):
    return 27.6113 - 0.145776*t + 0.0657895*t**2 - 0.00196133*t**3 + 3.91021e-5*t**4 - 4.40397e-7*t**5 + 2.80813e-9*t**6 - 1.01645e-11*t**7 + 1.94942e-14*t**8 - 1.53729e-17*t**9

def speed_mission_altitude(t):
    return 31.0556 - 0.343199*t + 0.0910034*t**2 - 0.00334765*t**3 + 7.12152e-05*t**4 - 8.67785e-07*t**5 + 6.08275e-09*t**6 -2.4314e-11*t**7 + 5.15945e-14*t**8 - 4.51568e-17*t**9

def load_mission_mach(csv_filename):
    csv = open(csv_filename, 'r')

    times = []
    machs = []

    for line in csv.readlines():
        vals = line.split(',')
        t = float(vals[0])     
        mach = float(vals[1])
        times.append(t)
        machs.append(mach)

    return (times, machs)

def std_atmosphere():
    alts = []
    rhos = []
    speed_of_sounds = []
    
    for h in range(0, 260001, 1000):
        rho = alt2density(h, alt_units='ft', density_units='kg/m**3')
        temp = isa2temp(0, h)
        speed_of_sound = temp2speed_of_sound(temp)
        
        alts.append(h)
        rhos.append(rho)
        speed_of_sounds.append(speed_of_sound)

    fig = plt.figure()
    host = fig.add_subplot(111)

    par1 = host.twinx()

    host.set_ylim(-0.05, 1.5)
    par1.set_ylim(400, 700)

    host.set_xlabel('Altitude (ft)')
    host.set_ylabel(r'Density $\frac{kg}{m^3}$')
    par1.set_ylabel('Speed of Sound (kt)')

    p1, = host.plot(alts, rhos, label=r'Density $\frac{kg}{m^3}$')
    p2, = par1.plot(alts, speed_of_sounds, color='r', label='Speed of sound (kt)')

    lns = [p1, p2]
    host.legend(handles=lns, loc='upper center')

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())

    plt.title('Standard Atmosphere')


def altitude_mission():
    fig = plt.figure()
    host = fig.add_subplot(111)

    par1 = host.twinx()
    par2 = host.twinx()
    
    host.set_ylim(0, 280)
    par1.set_ylim(0, 7)
    par2.set_ylim(0, 30)

    host.set_xlabel('Time (s)')
    host.set_ylabel('Altitude (1000 ft)')
    par1.set_ylabel('Mach')
    par2.set_ylabel('Dynamic Pressure (kPa)')

    times = []
    maxq = 0
    maxq_time = 0
    maxq_mach = 0
    maxq_alt = 0

    # Altitude
    alts = []

    for t in range(0, 261, 1):
        alt = altitude_mission_altitude(t)
        times.append(t)
        alts.append(alt)    

    # Mach
    mach_times, machs_raw = load_mission_mach('x-15-altitude-mission-mach.csv')    
    machs = []
    for t in range(0, 261, 1):
        mach = np.interp(t, mach_times, machs_raw)
        machs.append(mach)

    # Dynamic pressure
    qs = []
    for i in range(0, len(times)):
        mach = machs[i]
        h = alts[i] * 1000

        rho = alt2density(h, alt_units='ft', density_units='kg/m**3')

        temp = isa2temp(0, h)
        speed_of_sound = temp2speed_of_sound(temp, speed_units='m/s')
        v = mach * speed_of_sound

        q = 0.5 * rho * v**2
        qs.append(q/1000)
        
        if q > maxq:
            maxq = q
            maxq_time = i
            maxq_mach = mach
            maxq_alt = h

    p1, = host.plot(times, alts, label='Altitude (1000 ft)')
    p2, = par1.plot(times, machs, color='r', label='Mach')
    p3, = par2.plot(times, qs, color='g', label='Dynamic Pressure (kPa)' )

    #plt.axvline(x=maxq_time)
    print(maxq_time, maxq_alt, maxq_mach, maxq/1000)

    lns = [p1, p2, p3]
    host.legend(handles=lns, loc='upper left')

    par2.spines['right'].set_position(('outward', 40)) 

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())

    plt.title('Altitude Mission')
    

def speed_mission():
    fig = plt.figure()
    host = fig.add_subplot(111)

    par1 = host.twinx()
    par2 = host.twinx()
    
    host.set_ylim(0, 280)
    par1.set_ylim(0, 7)
    par2.set_ylim(0, 30)

    host.set_xlabel('Time (s)')
    host.set_ylabel('Altitude (1000 ft)')
    par1.set_ylabel('Mach')
    par2.set_ylabel('Dynamic Pressure (kPa)')

    times = []
    times = []
    maxq = 0
    maxq_time = 0
    maxq_mach = 0
    maxq_alt = 0

    # Altitude
    alts = []

    for t in range(0, 261, 1):
        alt = speed_mission_altitude(t)
        times.append(t)
        alts.append(alt)    

    # Mach
    mach_times, machs_raw = load_mission_mach('x-15-speed-mission-mach.csv')    
    machs = []
    for t in range(0, 261, 1):
        mach = np.interp(t, mach_times, machs_raw)
        machs.append(mach)

    # Dynamic pressure
    qs = []
    for i in range(0, len(times)):
        mach = machs[i]
        h = alts[i] * 1000

        rho = alt2density(h, alt_units='ft', density_units='kg/m**3')

        temp = isa2temp(0, h)
        speed_of_sound = temp2speed_of_sound(temp, speed_units='m/s')
        v = mach * speed_of_sound

        q = 0.5 * rho * v**2
        qs.append(q/1000)
        
        if q > maxq:
            maxq = q
            maxq_time = i
            maxq_mach = mach
            maxq_alt = h

    p1, = host.plot(times, alts, label='Altitude (1000 ft)')
    p2, = par1.plot(times, machs, color='r', label='Mach')
    p3, = par2.plot(times, qs, color='g', label='Dynamic Pressure (kPa)' )

    #plt.axvline(x=maxq_time)
    print(maxq_time, maxq_alt, maxq_mach, maxq/1000)

    lns = [p1, p2, p3]
    host.legend(handles=lns, loc='upper left')

    par2.spines['right'].set_position(('outward', 40)) 

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())

    plt.title('Speed Mission')
    

def sr71():
    rho = alt2density(80000, alt_units='ft', density_units='kg/m**3')
    temp = isa2temp(0, 80000)
    speed_of_sound = temp2speed_of_sound(temp, speed_units='m/s')
    mach = 3.5
    v = mach * speed_of_sound
    q = 0.5 * rho * v**2
    
    print(f'SR71: 80,000ft Mach 3.5 : {q/1000}kPa')


std_atmosphere()
altitude_mission()
speed_mission()
sr71()


plt.show()