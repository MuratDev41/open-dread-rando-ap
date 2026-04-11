from .Items import item_table, item_name_to_id, item_frequencies
from .Locations import location_table, location_name_to_id
from .Options import MetroidDreadOptions
from .Regions import create_regions
from .Rules import set_rules
from worlds.AutoWorld import World, WebWorld
import os
import json


class MetroidDreadWeb(WebWorld):
    theme = "ocean"


class MetroidDreadWorld(World):
    """
    Metroid Dread is an action-adventure game in which players control bounty hunter Samus Aran 
    as she explores the planet ZDR.
    """
    game = "Metroid Dread"
    topology_present = True
    web = MetroidDreadWeb()

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    options_dataclass = MetroidDreadOptions

    def create_items(self):
        item_pool = []
        for name, data in item_table.items():
            if data.quantity > 0:
                for _ in range(data.quantity):
                    item_pool.append(self.create_item(name))
            elif name in item_frequencies:
                for _ in range(item_frequencies[name]):
                    item_pool.append(self.create_item(name))

        # Pad with filler to match location count
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        deficit = total_locations - len(item_pool)
        if deficit > 0:
            for _ in range(deficit):
                item_pool.append(self.create_item("Missile Tank"))
        
        self.multiworld.itempool += item_pool

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def set_rules(self):
        set_rules(self, self.player)

    def fill_slot_data(self):
        return {
            "goal": self.options.goal.value,
        }

    def generate_output(self, output_directory: str):
        import json
        from .Locations import location_table
        from .Items import item_table

        item_model_map = {
            "Morph Ball": ["powerup_morphball"],
            "Bomb": ["powerup_bomb"],
            "Cross Bomb": ["powerup_crossbomb"],
            "Power Bomb": ["powerup_powerbomb"],
            "Charge Beam": ["powerup_chargebeam"],
            "Wide Beam": ["powerup_widebeam"],
            "Plasma Beam": ["powerup_plasmabeam"],
            "Wave Beam": ["powerup_wavebeam"],
            "Diffusion Beam": ["powerup_diffusionbeam"],
            "Grapple Beam": ["powerup_grapplebeam"],
            "Missile Launcher": ["powerup_missile"],
            "Super Missile": ["powerup_supermissile"],
            "Ice Missile": ["powerup_icemissile"],
            "Storm Missile": ["powerup_stormmissile"],
            "Phantom Cloak": ["powerup_opticcamo"],
            "Flash Shift": ["powerup_ghostaura"],
            "Pulse Radar": ["powerup_sonar"],
            "Spider Magnet": ["powerup_spidermagnet"],
            "Spin Boost": ["powerup_doublejump"],
            "Space Jump": ["powerup_spacejump"],
            "Screw Attack": ["powerup_screwattack"],
            "Varia Suit": ["powerup_variasuit"],
            "Gravity Suit": ["powerup_gravitysuit"],
            "Energy Tank": ["item_energytank"],
            "Power Bomb Expansion": ["item_powerbombtank"],
            "Missile Tank": ["item_missiletank"],
            "Missile Tank Plus": ["item_missiletankplus"],
            "Energy Part": ["item_energyfragment"],
        }

        patch_data = {
            "configuration_identifier": f"AP_{self.multiworld.seed_name}",
            "mod_compatibility": "ryujinx",
            "mod_category": "romfs",
            "enable_remote_lua": True,
            "pickups": []
        }

        # Map Archipelago Items to Patcher internal IDs (strings)
        item_name_to_id = {
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
            "Energy Tank": "ITEM_ENERGY_TANKS",
            "Power Bomb Expansion": "ITEM_WEAPON_POWER_BOMB_MAX",
            "Missile Tank": "ITEM_WEAPON_MISSILE_MAX",
            "Missile Tank Plus": "ITEM_WEAPON_MISSILE_MAX",
            "Energy Part": "ITEM_LIFE_SHARDS",
        }

        for location in self.multiworld.get_locations(self.player):
            if location.name not in location_table:
                continue
            
            loc_data = location_table[location.name]
            item = location.item
            
            is_remote = item.player != self.player
            
            # Use specific item name or remote placeholder
            patcher_item_name = item_name_to_id.get(item.name, "ITEM_NONE")
            if "Artifact" in item.name:
                patcher_item_name = f"ITEM_RANDO_ARTIFACT_{item.name.split()[-1]}"

            model = item_model_map.get(item.name, ["itemsphere"])
            
            pickup = {
                "pickup_type": loc_data.pickup_type if hasattr(loc_data, "pickup_type") else "actor",
                "caption": f"{item.name} from {self.multiworld.get_player_name(item.player)}" if is_remote else f"{item.name}",
                "resources": [[{"item_id": patcher_item_name, "quantity": 1}]],
                "model": model,
                "is_remote": is_remote
            }
            
            if pickup["pickup_type"] == "actor":
                pickup["pickup_actor"] = {
                    "scenario": loc_data.scenario,
                    "actor": loc_data.actor
                }
            else:
                pickup["pickup_lua_callback"] = {
                    "scenario": loc_data.scenario,
                    "function": loc_data.actor
                }
                pickup["pickup_actordef"] = loc_data.actordef # I'll need to check if I added this to Locations.py
                pickup["pickup_string_key"] = f"STR_ID_{location.name.replace(' ', '_')}"

            patch_data["pickups"].append(pickup)

        filename = f"AP_{self.multiworld.seed_name}_P{self.player}_{self.multiworld.get_player_name(self.player)}.json"
        with open(os.path.join(output_directory, filename), "w") as f:
            json.dump(patch_data, f, indent=4)

    def create_item(self, name: str):
        data = item_table[name]
        classification = ItemClassification.progression if data.progression else ItemClassification.filler
        return MetroidDreadItem(name, classification, data.code, self.player)


from .Items import ItemData
from BaseClasses import Item, ItemClassification


class MetroidDreadItem(Item):
    game: str = "Metroid Dread"

from worlds.LauncherComponents import components, Component, Type, launch as launch_component

def launch_client(*args):
    import sys
    import os
    world_dir = os.path.dirname(__file__)
    if world_dir not in sys.path:
        sys.path.insert(0, world_dir)
    from .Client import launch
    launch_component(launch, name="Metroid Dread Client", args=args)

components.append(Component('Metroid Dread Client', func=launch_client, component_type=Type.CLIENT, game_name='Metroid Dread', supports_uri=True, description="Connect to the Archipelago server and sync items with your game."))
