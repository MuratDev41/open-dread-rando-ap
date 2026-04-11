from dataclasses import dataclass
from Options import Choice, DeathLink, PerGameCommonOptions


class Goal(Choice):
    """What is the goal of the game?
    Bosses: Defeat Raven Beak.
    Artifacts: Collect all 12 artifacts to unlock the path to the final boss."""
    display_name = "Goal"
    option_bosses = 0
    option_artifacts = 1
    default = 0


@dataclass
class MetroidDreadOptions(PerGameCommonOptions):
    goal: Goal
    death_link: DeathLink
