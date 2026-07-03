extends SceneTree

func _init():
    print("\n[+] 04901 SPATIAL MATRIX: Headless Engine Online")
    print("[*] Processing spatial vectors...")

    # Define the Waterville lattice origin point (mapped to X, Y, Z)
    # X = Latitude, Y = Altitude/Elevation, Z = Longitude
    var lattice_origin = Vector3(44.5520, 0.0, -69.6317)
    
    # Simulating an incoming telemetry vector from the LEO/SDR pipeline
    var signal_vector = Vector3(44.5550, 150.0, -69.6300)
    
    # Calculate the precise 3D spatial delta
    var spatial_delta = lattice_origin.distance_to(signal_vector)
    
    print("[!] Telemetry Mapped.")
    print("    -> Origin Node: ", lattice_origin)
    print("    -> Signal Node: ", signal_vector)
    print("    -> 3D Spatial Delta (Distance): ", spatial_delta)
    
    print("\n[*] Matrix calculations complete. Shutting down spatial core.")
    quit()
