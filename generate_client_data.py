import json

with open("tests/test_files/patcher_files/starter_preset_patcher.json", "r") as f:
    data = json.load(f)

location_to_ap_id = {}
ap_id_to_item_str = {}

# Location Mapping: scenario_actor -> AP ID
start_id = 80000
for i, pickup in enumerate(data["pickups"]):
    if pickup["pickup_type"] == "actor":
        scenario = pickup["pickup_actor"]["scenario"]
        actor = pickup["pickup_actor"]["actor"]
    elif "pickup_lua_callback" in pickup:
        scenario = pickup["pickup_lua_callback"]["scenario"]
        actor = pickup["pickup_lua_callback"]["function"]
    else:
        continue # Should not happen based on schema
    
    key = f"{scenario}_{actor}"
    location_to_ap_id[key] = start_id + i

# Item Mapping: AP ID -> In-Game Item ID
items = {
    "Morph Ball": "ITEM_MORPH_BALL",
    "Bomb": "ITEM_BOMB",
    "Cross Bomb": "ITEM_CROSS_BOMB",
    "Power Bomb": "ITEM_POWER_BOMB",
    "Charge Beam": "ITEM_WEAPON_CHARGE_BEAM",
    "Wide Beam": "ITEM_WEAPON_WIDE_BEAM",
    "Plasma Beam": "ITEM_WEAPON_PLASMA_BEAM",
    "Wave Beam": "ITEM_WEAPON_WAVE_BEAM",
    "Diffusion Beam": "ITEM_WEAPON_DIFFUSION_BEAM",
    "Grapple Beam": "ITEM_WEAPON_GRAPPLE_BEAM",
    "Missile Launcher": "ITEM_WEAPON_MISSILE_LAUNCHER",
    "Super Missile": "ITEM_WEAPON_SUPER_MISSILE",
    "Ice Missile": "ITEM_WEAPON_ICE_MISSILE",
    "Storm Missile": "ITEM_WEAPON_STORM_MISSILE",
    "Phantom Cloak": "ITEM_OPTIC_CAMOUFLAGE",
    "Flash Shift": "ITEM_GHOST_AURA",
    "Pulse Radar": "ITEM_SONAR",
    "Spider Magnet": "ITEM_MAGNET_GLOVE",
    "Spin Boost": "ITEM_DOUBLE_JUMP",
    "Space Jump": "ITEM_SPACE_JUMP",
    "Screw Attack": "ITEM_SCREW_ATTACK",
    "Varia Suit": "ITEM_VARIA_SUIT",
    "Gravity Suit": "ITEM_GRAVITY_SUIT",
}

# Add Archipelago IDs for items
ap_item_to_ingame = {}
for i, (name, ingame) in enumerate(items.items()):
    ap_item_to_ingame[80000 + i] = ingame

# Expanded item list (expansions)
ap_item_to_ingame[80023] = "ITEM_ENERGY_TANKS"
ap_item_to_ingame[80024] = "ITEM_WEAPON_POWER_BOMB_MAX"
ap_item_to_ingame[80025] = "ITEM_WEAPON_MISSILE_MAX"
ap_item_to_ingame[80026] = "ITEM_WEAPON_MISSILE_MAX" # Tank Plus
ap_item_to_ingame[80027] = "ITEM_LIFE_SHARDS"

# Artifacts
for i in range(12):
    ap_item_to_ingame[80028 + i] = f"ITEM_RANDO_ARTIFACT_{i+1}"

with open("MetroidDreadData.py", "w") as f:
    f.write("LOCATION_MAPPING = " + json.dumps(location_to_ap_id, indent=4) + "\n\n")
    f.write("ITEM_MAPPING = " + json.dumps(ap_item_to_ingame, indent=4) + "\n")
