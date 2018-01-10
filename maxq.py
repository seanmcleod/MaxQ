from std_atm import *
import matplotlib.pyplot as plt


def std_atmosphere_densities(start, end, increment):
    alts = []
    rhos = []

    for h in range(start, end, increment):
        rho = alt2density(h, alt_units='m', density_units='kg/m**3')
        alts.append(h/1000)
        rhos.append(rho)

    return (alts, rhos)


def spacex_jcsat14():
    (alts, rhos) = std_atmosphere_densities(0, 66000, 500)

    spacex_alts = []
    velocities = []
    velocities_squared = []
    qs = []

    csv = open('SpaceX - JCSAT14 Launch.csv', 'r')

    for line in csv.readlines():
        vals = line.split(',')
        alt = float(vals[2]) 
        spacex_alts.append(alt)
        velocity = float(vals[1])
        velocities.append(velocity)
        velocities_squared.append(velocity*velocity)

        rho = alt2density(alt, alt_units='km', density_units='kg/m**3')
        velocity_ms = (velocity * 1000) / (60 * 60)
        dynamic_pressure = 0.5 * rho * (velocity_ms * velocity_ms)
        qs.append(dynamic_pressure / 1000)  # kilo pascals

    fig = plt.figure()
    host = fig.add_subplot(111)

    par1 = host.twinx()
    par2 = host.twinx()

    host.set_ylim(-0.05, 1.5)
    par1.set_ylim(0, 70000000)
    par2.set_ylim(0, 32)

    host.set_xlabel('Altitude (km)')
    host.set_ylabel('Density')
    par1.set_ylabel('Velocity Squared')
    par2.set_ylabel('Dynamic Pressure')

    p1, = host.plot(alts, rhos, label='Density (kg/m^3)')
    p2, = par1.plot(spacex_alts, velocities_squared, color='r', label='Velocity Squared (km/h)')
    p3, = par2.plot(spacex_alts, qs, color='g', label='Dynamic Pressure (kPa)')

    lns = [p1, p2, p3]
    host.legend(handles=lns, loc='upper center')

    par2.spines['right'].set_position(('outward', 60))      

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())

    plt.title('SpaceX - JCSAT14 - Standard Atmosphere')


def nasa_sts124():
    (alts, rhos) = std_atmosphere_densities(0, 66000, 500)
    
    nasa_alts = []
    nasa_throttles = []
    velocities = []
    velocities_squared = []
    qs = []

    csv = open('NASA Shuttle - STS124 Launch.csv', 'r')

    for line in csv.readlines():
        vals = line.split(',')
        throttle = float(vals[1])
        alt = float(vals[2]) 
        velocity = float(vals[3])
        
        nasa_alts.append(alt)
        nasa_throttles.append(throttle)

        velocities.append(velocity)
        velocities_squared.append(velocity*velocity)

        rho = alt2density(alt, alt_units='km', density_units='kg/m**3')
        velocity_ms = (velocity * 1000) / (60 * 60)
        dynamic_pressure = 0.5 * rho * (velocity_ms * velocity_ms)
        qs.append(dynamic_pressure / 1000)  # kilo pascals

    fig = plt.figure()
    host = fig.add_subplot(111)

    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()

    host.set_ylim(-0.05, 1.5)
    par1.set_ylim(0, 30000000)
    par2.set_ylim(0, 40)
    par3.set_ylim(0, 110)

    host.set_xlabel('Altitude (km)')
    host.set_ylabel('Density')
    par1.set_ylabel('Velocity Squared')
    par2.set_ylabel('Dynamic Pressure')
    par3.set_ylabel('Throttle')

    p1, = host.plot(alts, rhos, label='Density (kg/m^3)')
    p2, = par1.plot(nasa_alts, velocities_squared, color='r', label='Velocity Squared (km/h)')
    p3, = par2.plot(nasa_alts, qs, color='g', label='Dynamic Pressure (kPa)')
    p4, = par3.plot(nasa_alts, nasa_throttles, color='black', label='Throttle (%)')

    lns = [p1, p2, p3, p4]
    host.legend(handles=lns, loc='center right')

    par2.spines['right'].set_position(('outward', 60))      

    # Move throttle axis to the left side    
    par3.spines['left'].set_position(('outward', 60))      
    par3.spines["left"].set_visible(True)
    par3.yaxis.set_label_position('left')
    par3.yaxis.set_ticks_position('left')

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())
    par3.yaxis.label.set_color(p4.get_color())

    plt.title('NASA - STS124 - Standard Atmosphere')


def airliner():
    (alts, rhos) = std_atmosphere_densities(0, 10500, 500)    

    # Convert from m to ft
    for i in range(0, len(alts)):
        alts[i] = alts[i] * 3280.84

    airliner_alts = []
    airliner_speeds = []
    qs = []

    csv = open('Airliner.csv', 'r')

    for line in csv.readlines():
        vals = line.split(',')
        alt = float(vals[0]) 
        velocity = float(vals[1])
        
        airliner_alts.append(alt)
        airliner_speeds.append(velocity)

        rho = alt2density(alt, alt_units='ft', density_units='kg/m**3')
        velocity_ms = velocity * 0.5144  # knots to m/s
        dynamic_pressure = 0.5 * rho * (velocity_ms * velocity_ms)
        qs.append(dynamic_pressure / 1000)  # kilo pascals

    fig = plt.figure()
    host = fig.add_subplot(111)

    par1 = host.twinx()
    par2 = host.twinx()

    host.set_ylim(-0.05, 1.5)
    par1.set_ylim(0, 700)
    par2.set_ylim(0, 30)

    host.set_xlabel('Altitude (ft)')
    host.set_ylabel('Density')
    par1.set_ylabel('Ground Speed')
    par2.set_ylabel('Dynamic Pressure')

    p1, = host.plot(alts, rhos, label='Density (kg/m^3)')
    p2, = par1.plot(airliner_alts, airliner_speeds, color='r', label='Ground Speed (kt)')
    p3, = par2.plot(airliner_alts, qs, color='g', label='Dynamic Pressure (kPa)')

    lns = [p1, p2, p3]
    host.legend(handles=lns, loc='center right')

    par2.spines['right'].set_position(('outward', 60))      

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())

    plt.title('Airliner - Standard Atmosphere')



spacex_jcsat14()
nasa_sts124()
airliner()

plt.show()