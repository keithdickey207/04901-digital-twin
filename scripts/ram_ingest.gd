extends SceneTree

func _init():
    print("\n[+] 04901 SPATIAL MATRIX: Persistent Point-Cloud Generator Online")
    var shm_path = "/dev/shm/sovereign_spikes.json"
    var obj_path = "user://04901_lattice.obj"

    if not FileAccess.file_exists(shm_path):
        print("[-] No neural spike data found in /dev/shm.")
        quit()
        return

    var file = FileAccess.open(shm_path, FileAccess.READ)
    var content = file.get_as_text()
    file.close()

    var json = JSON.new()
    var error = json.parse(content)

    if error == OK:
        var data = json.data
        var x = float(data["x_lat"])
        var y = float(data["y_alt_spikes"])
        var z = float(data["z_lon"])
        
        var vertex_string = "v %f %f %f\n" % [x, y, z]
        
        var obj_file
        if FileAccess.file_exists(obj_path):
            obj_file = FileAccess.open(obj_path, FileAccess.READ_WRITE)
            obj_file.seek_end()
        else:
            obj_file = FileAccess.open(obj_path, FileAccess.WRITE)
            obj_file.store_string("# 04901 5D Loom Point Cloud Lattice\n")
            
        obj_file.store_string(vertex_string)
        obj_file.close()

        print("[!] Neural Telemetry Engraved to Lattice -> " + vertex_string.strip_edges())
        print("[*] Point-cloud geometry updated.")
    else:
        print("[-] JSON Parse Error.")

    quit()
