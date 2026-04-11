from .Items import item_table, item_name_to_id, item_frequencies
from .Locations import location_table, location_name_to_id
from .Options import MetroidDreadOptions
from .Regions import create_regions
from .Rules import set_rules
from worlds.AutoWorld import World, WebWorld
import os
import json
import uuid


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
            "starting_location": {
                "scenario": "s010_cave",
                "actor": "StartPoint0"
            },
            "starting_items": {},
            "starting_text": [[]],
            "energy_per_tank": 100,
            "immediate_energy_parts": True,
            "layout_uuid": str(uuid.uuid5(uuid.NAMESPACE_DNS, f"AP_{self.multiworld.seed_name}")),
            "has_flash_upgrades": False,
            "has_speed_upgrades": False,
            "hints": [],
            "text_patches": {},
            "spoiler_log": {},
            "elevators": [],
            "door_patches": [],
            "tile_group_patches": [],
            "new_spawn_points": [],
            "mass_delete_actors": {
                "to_remove": []
            },
            "actor_patches": {},
            "objective": {
                "required_artifacts": 0,
                "hints": []
            },
            "game_patches": {
                "raven_beak_damage_table_handling": "consistent_low",
                "remove_grapple_blocks_hanubia_shortcut": True,
                "remove_grapple_block_path_to_itorash": True,
                "default_x_released": False,
                "enable_experiment_boss": True,
                "warp_to_start": True,
                "nerf_power_bombs": False,
                "remove_water_platform_water": True,
                "remove_early_cloak_water": "right_only",
                "remove_arbitrary_enky": "unmodified"
            },
            "constant_environment_damage": {
                "heat": None,
                "cold": None,
                "lava": None
            },
            "cosmetic_patches": {
                "config": {},
                "lua": {
                    "custom_init": {
                        "show_dna_in_hud": False,
                        "enable_death_counter": False,
                        "enable_room_name_display": "NEVER"
                    },
                    "camera_names_dict": {}
                },
                "shield_versions": {
                    "ice_missile": "DEFAULT",
                    "diffusion_beam": "DEFAULT",
                    "storm_missile": "DEFAULT",
                    "bomb": "DEFAULT",
                    "cross_bomb": "DEFAULT",
                    "power_bomb": "DEFAULT",
                    "closed": "DEFAULT"
                }
            },
            "pickups": []
        }

        # Map Archipelago Items to Patcher internal IDs (strings)
        item_name_to_id = {
            "Morph Ball": "ITEM_MORPH_BALL",
            "Bomb": "ITEM_WEAPON_BOMB",
            "Cross Bomb": "ITEM_WEAPON_LINE_BOMB",
            "Power Bomb": "ITEM_WEAPON_POWER_BOMB",
            "Charge Beam": "ITEM_WEAPON_CHARGE_BEAM",
            "Wide Beam": "ITEM_WEAPON_WIDE_BEAM",
            "Plasma Beam": "ITEM_WEAPON_PLASMA_BEAM",
            "Wave Beam": "ITEM_WEAPON_WAVE_BEAM",
            "Diffusion Beam": "ITEM_WEAPON_DIFFUSION_BEAM",
            "Grapple Beam": "ITEM_WEAPON_GRAPPLE_BEAM",
            "Missile Launcher": "ITEM_WEAPON_MISSILE_LAUNCHER",
            "Super Missile": "ITEM_WEAPON_SUPER_MISSILE",
            "Ice Missile": "ITEM_WEAPON_ICE_MISSILE",
            "Storm Missile": "ITEM_MULTILOCKON",
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
            
            ptype = "actor"
            actordef = None
            if list(filter(loc_data.name.endswith, ["Hanubia EMMI", "Artaria EMMI", "Ferenia EMMI", "Cataris EMMI", "Ghavoran EMMI", "Dairon EMMI"])):
                ptype = "emmi"
                actordef = {
                    "Hanubia EMMI": "actors/characters/emmyshipyard/charclasses/emmyshipyard.bmsad",
                    "Artaria EMMI": "actors/characters/emmycave/charclasses/emmycave.bmsad",
                    "Ferenia EMMI": "actors/characters/emmysanc/charclasses/emmysanc.bmsad",
                    "Cataris EMMI": "actors/characters/emmymagma/charclasses/emmymagma.bmsad",
                    "Ghavoran EMMI": "actors/characters/emmyforest/charclasses/emmyforest.bmsad",
                    "Dairon EMMI": "actors/characters/emmylab/charclasses/emmylab.bmsad"
                }[loc_data.name.split(" - ")[-1]]
            elif loc_data.name in ["Ghavoran - Escue", "Ghavoran - Golzuna"]:
                ptype = "corex"
                actordef = {
                    "Ghavoran - Escue": "actors/characters/core_x_superquetzoa/charclasses/core_x_superquetzoa.bmsad",
                    "Ghavoran - Golzuna": "actors/characters/core_x/charclasses/core_x.bmsad"
                }[loc_data.name]
            elif loc_data.name == "Artaria - Scorpius":
                ptype = "corpius"
                actordef = "actors/characters/scorpius/charclasses/scorpius.bmsad"
            elif loc_data.name in ["Cataris - Kraid", "Burenia - Drogyga", "Cataris - Experiment No. Z-57"]:
                ptype = "cutscene"

            pickup = {
                "pickup_type": ptype,
                "caption": f"{item.name} from {self.multiworld.get_player_name(item.player)}" if is_remote else f"{item.name}",
                "resources": [[{"item_id": patcher_item_name, "quantity": 1}]],
                "model": model,
                "map_icon": {"icon_id": model[0]},
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
                if actordef is not None:
                    pickup["pickup_actordef"] = actordef
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
