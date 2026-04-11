from worlds.generic.Rules import set_rule, add_rule

def set_rules(world, player):
    multiworld = world.multiworld

    # --- Item-to-Item Logic ---
    # (Simplified for AP logic mapping)
    
    # --- Location Logic ---
    # We use a set of lambda functions to check for item possession
    

    # Artaria Logic
    set_rule(multiworld.get_location("Artaria - ItemSphere_ChargeBeam", player), 
             lambda state: True) # Usually first item
    
    set_rule(multiworld.get_location("Artaria - ItemSphere_ScrewAttack", player), 
             lambda state: state.has("Space Jump", player) or state.has("Gravity Suit", player))

    # Cataris Logic
    set_rule(multiworld.get_location("Cataris - Experiment No. Z-57", player), 
             lambda state: state.has("Varia Suit", player) and state.has("Plasma Beam", player))
    
    set_rule(multiworld.get_location("Cataris - Kraid", player), 
             lambda state: state.has("Charge Beam", player) and state.has("Wide Beam", player))

    # Burenia Logic
    set_rule(multiworld.get_location("Burenia - itemsphere_gravitysuit", player), 
             lambda state: state.has("Space Jump", player) and state.has("Ice Missile", player))

    # General Item Requirements based on location names containing tags
    for location in multiworld.get_locations(player):
        if location.game != "Metroid Dread":
            continue
        
        # Entrance/Region Access Rules
        # (This is handled by Region connections, but we can add specific rules here)
        
        # Specific item requirements based on common dread names
        if "Power Bomb" in location.name:
            add_rule(location, lambda state: state.has("Power Bomb", player))
        if "Missile Tank" in location.name:
            add_rule(location, lambda state: state.has("Missile Launcher", player))

    # --- Region Traversal Rules ---
    # These effectively gate entire areas
    
    # Cataris (Heat areas)
    for entrance in multiworld.get_region("Cataris", player).exits:
        add_rule(entrance, lambda state: state.has("Varia Suit", player))

    # Itorash Access (Final Boss)
    if world.options.goal == 1:  # Artifacts
        set_rule(multiworld.get_entrance("Hanubia to Itorash", player),
                 lambda state: state.has_all({f"Artifact {i+1}" for i in range(12)}, player))
    else:
        set_rule(multiworld.get_entrance("Hanubia to Itorash", player),
                 lambda state: state.has("Screw Attack", player) and state.has("Gravity Suit", player) and state.has("Wave Beam", player))

    world.multiworld.completion_condition[player] = lambda state: state.has("Hyper Beam", player) or state.has("Screw Attack", player) # Standard fallback

