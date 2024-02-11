import krpc


file = open("file_velocity.txt", "w")

conn = krpc.connect("graphic_velocity")
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
        angle = vessel.flight().pitch
        velocity = vessel.flight(vessel.orbit.body.reference_frame).speed
        file.write(f"{time_flight} {angle} {velocity}\n")  
        file.flush()
