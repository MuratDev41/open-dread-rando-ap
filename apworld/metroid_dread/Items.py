from typing import NamedTuple, Dict, Optional


class ItemData(NamedTuple):
    name: str
    code: Optional[int]
    progression: bool
    quantity: int = 1


item_table: Dict[str, ItemData] = {
    "Morph Ball": ItemData("Morph Ball", 80000, True),
    "Bomb": ItemData("Bomb", 80001, True),
    "Cross Bomb": ItemData("Cross Bomb", 80002, True),
    "Power Bomb": ItemData("Power Bomb", 80003, True),
    "Charge Beam": ItemData("Charge Beam", 80004, True),
    "Wide Beam": ItemData("Wide Beam", 80005, True),
    "Plasma Beam": ItemData("Plasma Beam", 80006, True),
    "Wave Beam": ItemData("Wave Beam", 80007, True),
    "Diffusion Beam": ItemData("Diffusion Beam", 80008, True),
    "Grapple Beam": ItemData("Grapple Beam", 80009, True),
    "Missile Launcher": ItemData("Missile Launcher", 80010, True),
    "Super Missile": ItemData("Super Missile", 80011, True),
    "Ice Missile": ItemData("Ice Missile", 80012, True),
    "Storm Missile": ItemData("Storm Missile", 80013, True),
    "Phantom Cloak": ItemData("Phantom Cloak", 80014, True),
    "Flash Shift": ItemData("Flash Shift", 80015, True),
    "Pulse Radar": ItemData("Pulse Radar", 80016, True),
    "Spider Magnet": ItemData("Spider Magnet", 80017, True),
    "Spin Boost": ItemData("Spin Boost", 80018, True),
    "Space Jump": ItemData("Space Jump", 80019, True),
    "Screw Attack": ItemData("Screw Attack", 80020, True),
    "Varia Suit": ItemData("Varia Suit", 80021, True),
    "Gravity Suit": ItemData("Gravity Suit", 80022, True),

    "Energy Tank": ItemData("Energy Tank", 80023, True, 0),  # Quantity 0 means it's an expansion
    "Power Bomb Expansion": ItemData("Power Bomb Expansion", 80024, False, 0),
    "Missile Tank": ItemData("Missile Tank", 80025, False, 0),
    "Missile Tank Plus": ItemData("Missile Tank Plus", 80026, False, 0),
    "Energy Part": ItemData("Energy Part", 80027, True, 0),

    "Artifact 1": ItemData("Artifact 1", 80028, True),
    "Artifact 2": ItemData("Artifact 2", 80029, True),
    "Artifact 3": ItemData("Artifact 3", 80030, True),
    "Artifact 4": ItemData("Artifact 4", 80031, True),
    "Artifact 5": ItemData("Artifact 5", 80032, True),
    "Artifact 6": ItemData("Artifact 6", 80033, True),
    "Artifact 7": ItemData("Artifact 7", 80034, True),
    "Artifact 8": ItemData("Artifact 8", 80035, True),
    "Artifact 9": ItemData("Artifact 9", 80036, True),
    "Artifact 10": ItemData("Artifact 10", 80037, True),
    "Artifact 11": ItemData("Artifact 11", 80038, True),
    "Artifact 12": ItemData("Artifact 12", 80039, True),
}

item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}

item_frequencies = {
    "Energy Tank": 12,
    "Power Bomb Expansion": 13,
    "Missile Tank": 40,
    "Missile Tank Plus": 10,
    "Energy Part": 24,
}
