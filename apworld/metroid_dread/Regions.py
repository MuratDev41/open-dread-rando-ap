from typing import List, Dict, Set
from worlds.AutoWorld import World
from BaseClasses import Region, Entrance, Location
from .Locations import location_table, LocationData


def create_regions(multiworld, player: int):
    regions: Dict[str, Region] = {}

    # Create regions
    region_names = [
        "Menu",
        "Artaria",
        "Cataris",
        "Dairon",
        "Burenia",
        "Ghavoran",
        "Elun",
        "Ferenia",
        "Hanubia",
        "Itorash",
    ]

    for name in region_names:
        regions[name] = Region(name, player, multiworld)
        multiworld.regions.append(regions[name])

    # Connect Menu to Artaria (Start)
    regions["Menu"].add_exits(["Artaria"])

    # Add locations to regions
    for name, data in location_table.items():
        region_name = name.split(" - ")[0]
        if region_name in regions:
            regions[region_name].locations.append(MetroidDreadLocation(player, name, data.code, regions[region_name]))

    # Actual Game Connections
    connect(multiworld, player, regions, "Artaria", "Cataris")
    connect(multiworld, player, regions, "Cataris", "Artaria")
    
    connect(multiworld, player, regions, "Artaria", "Burenia")
    connect(multiworld, player, regions, "Burenia", "Artaria")
    
    connect(multiworld, player, regions, "Cataris", "Dairon")
    connect(multiworld, player, regions, "Dairon", "Cataris")

    connect(multiworld, player, regions, "Dairon", "Artaria")
    connect(multiworld, player, regions, "Artaria", "Dairon")

    connect(multiworld, player, regions, "Dairon", "Burenia")
    connect(multiworld, player, regions, "Burenia", "Dairon")

    connect(multiworld, player, regions, "Dairon", "Ghavoran")
    connect(multiworld, player, regions, "Ghavoran", "Dairon")

    connect(multiworld, player, regions, "Dairon", "Ferenia")
    connect(multiworld, player, regions, "Ferenia", "Dairon")

    connect(multiworld, player, regions, "Burenia", "Ghavoran")
    connect(multiworld, player, regions, "Ghavoran", "Burenia")

    connect(multiworld, player, regions, "Cataris", "Ghavoran")
    connect(multiworld, player, regions, "Ghavoran", "Cataris")

    connect(multiworld, player, regions, "Ghavoran", "Elun")
    connect(multiworld, player, regions, "Elun", "Ghavoran")

    connect(multiworld, player, regions, "Ghavoran", "Ferenia")
    connect(multiworld, player, regions, "Ferenia", "Ghavoran")

    connect(multiworld, player, regions, "Ferenia", "Hanubia")
    connect(multiworld, player, regions, "Hanubia", "Ferenia")

    connect(multiworld, player, regions, "Hanubia", "Itorash")
    connect(multiworld, player, regions, "Itorash", "Hanubia")


def connect(multiworld, player: int, regions: Dict[str, Region], source: str, target: str):
    source_region = regions[source]
    target_region = regions[target]
    connection = Entrance(player, f"{source} to {target}", source_region)
    source_region.exits.append(connection)
    connection.connect(target_region)


from BaseClasses import Location


class MetroidDreadLocation(Location):
    game: str = "Metroid Dread"
