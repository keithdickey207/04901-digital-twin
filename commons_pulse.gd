extends Node

const API_STATUS_URL = "http://localhost:8000/api/operations/status"
@onready var http_request = HTTPRequest.new()

func _ready():
	add_child(http_request)
	http_request.request_completed.connect(_on_request_completed)
	
	poll_operational_state()
	
	var poll_timer = Timer.new()
	poll_timer.wait_time = 5.0
	poll_timer.autostart = true
	poll_timer.timeout.connect(poll_operational_state)
	add_child(poll_timer)

func poll_operational_state():
	print("[*] Polling local operational API...")
	var error = http_request.request(API_STATUS_URL)
	if error != OK:
		push_error("[-] Failed to execute API request.")

func _on_request_completed(result, response_code, headers, body):
	if response_code == 200:
		var json = JSON.new()
		var parse_result = json.parse(body.get_string_from_utf8())
		
		if parse_result == OK:
			var response = json.get_data()
			var assets = response["assets"]
			
			for asset in assets:
				var id = asset["asset_id"]
				var status = asset["asset_status"]
				
				var coords = asset["geo_coordinates"].split(",")
				var lat = coords[0].to_float()
				var lon = coords[1].to_float()
				
				update_spatial_asset(id, status, lat, lon)
		else:
			push_error("[-] JSON Parse Error: " + json.get_error_message())
	else:
		print("[-] API unreachable. Code: ", response_code)

func update_spatial_asset(asset_id, status, lat, lon):
	print("[+] Kinetic Update: ", asset_id, " | Status: ", status, " | Location: ", lat, ", ", lon)
# The real-world coordinates you want to treat as the absolute center (0,0,0) of your 3D world
# Let's anchor it to the center of Waterville, Maine
const CENTER_LAT = 44.5520
const CENTER_LON = -69.6317

# Scaling factor: How many game grid units (meters) equal roughly one degree of earth curve
const METERS_PER_DEGREE_LAT = 111132.0

func gps_to_vector3(lat: float, lon: float) -> Vector3:
	# 1. Calculate the difference from our world anchor point
	var lat_diff = lat - CENTER_LAT
	var lon_diff = lon - CENTER_LON
	
	# 2. Convert degrees into approximate local flat map meters
	var z_pos = -lat_diff * METERS_PER_DEGREE_LAT # Negative because Godot -Z is forward
	
	# Longitude length depends on how far north/south you are on the globe
	var meters_per_degree_lon = METERS_PER_DEGREE_LAT * cos(deg_to_rad(CENTER_LAT))
	var x_pos = lon_diff * meters_per_degree_lon
	
	# 3. Return the 3D position vector (Y is altitude, keeping it on the ground at 0)
	return Vector3(x_pos, 0.0, z_pos)
