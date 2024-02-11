import krpc


file = open("file_altitude.txt", "w")

conn = krpc.connect("graphic_altitude")
vessel = conn.space_center.active_vessel
engines = vessel.parts.engines

launch_time = conn.add_stream(getattr, engines[5], 'active')
current_time = conn.add_stream(getattr, conn.space_center, 'ut')

while not launch_time():
    pass

mission_start_time = conn.space_center.ut 
actual_time = mission_start_time

while True:
    if current_time() - actual_time >= 0.1:
        actual_time = current_time()
        time_flight = actual_time - mission_start_time
        altitude = vessel.flight().surface_altitude
        angle = vessel.flight().pitch
        file.write(f"{time_flight} {altitude} {angle}\n")  
        file.flush()
