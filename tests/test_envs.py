"""Unit tests for all of the envs"""

import unittest

import numpy as np

from social_dilemmas.envs.agent import (
    BASE_ACTIONS,
    CLEANUP_ACTIONS,
    HARVEST_ACTIONS,
    Agent,
    CleanupAgent,
    HarvestAgent,
)
from social_dilemmas.envs.cleanup import CleanupEnv
from social_dilemmas.envs.gym.discrete_with_dtype import DiscreteWithDType
from social_dilemmas.envs.harvest import HarvestEnv
from social_dilemmas.envs.map_env import MapEnv

# map actions to appropriate numbers
ACTION_MAP = {y: x for x, y in BASE_ACTIONS.items()}
HARVEST_ACTION_MAP = {y: x for x, y in HARVEST_ACTIONS.items()}
CLEANUP_ACTION_MAP = {y: x for x, y in CLEANUP_ACTIONS.items()}

# Maps for any env
BASE_MAP_1 = [
    "@@@@@@@",
    "@     @",
    "@     @",
    "@     @",
    "@     @",
    "@     @",
    "@@@@@@@",
]
TEST_MAP_1 = np.array(
    [
        [b"@"] * 7,
        [b"@"] + [b" "] * 5 + [b"@"],
        [b"@"] + [b" "] * 5 + [b"@"],
        [b"@"] + [b" "] * 5 + [b"@"],
        [b"@"] + [b" "] * 5 + [b"@"],
        [b"@"] + [b" "] * 5 + [b"@"],
        [b"@"] * 7,
    ]
)

FIRE_RANGE_MAP = np.array(
    [
        [b"@"] * 13,
        [b"@"] + [b" "] * 11 + [b"@"],
        [b"@"] + [b" "] * 11 + [b"@"],
        [b"@"] + [b" "] * 11 + [b"@"],
        [b"@"] + [b" "] * 11 + [b"@"],
        [b"@"] + [b" "] * 11 + [b"@"],
        [b"@"] + [b" "] * 11 + [b"@"],
        [b"@"] + [b" "] * 11 + [b"@"],
        [b"@"] + [b" "] * 11 + [b"@"],
        [b"@"] + [b" "] * 11 + [b"@"],
        [b"@"] + [b" "] * 11 + [b"@"],
        [b"@"] + [b" "] * 11 + [b"@"],
        [b"@"] * 13,
    ]
)
# basic empty map with no apples
BASE_MAP_2 = ["@@@@@@", "@ P  @", "@    @", "@    @", "@   P@", "@@@@@@"]
TEST_MAP_2 = np.array(
    [
        [b"@"] * 6,
        [b"@"] + [b" "] * 4 + [b"@"],
        [b"@"] + [b" "] * 4 + [b"@"],
        [b"@"] + [b" "] * 4 + [b"@"],
        [b"@"] + [b" "] * 2 + [b"A"] + [b" "] + [b"@"],
        [b"@"] * 6,
    ]
)
# Maps for Harvest
MINI_HARVEST_MAP = [
    "@@@@@@",
    "@ P  @",
    "@  AA@",
    "@  AA@",
    "@  AP@",
    "@@@@@@",
]

# Maps for Cleanup
MINI_CLEANUP_MAP = [
    "@@@@@@",
    "@ P  @",
    "@H BB@",
    "@R BB@",
    "@S BP@",
    "@@@@@@",
]
# Check that apples spawn correctly in cleanup
APPLE_SPAWN_MAP_CLEANUP = [
    "@@@@@@",
    "@ P  @",
    "@  BB@",
    "@  BB@",
    "@  BP@",
    "@@@@@@",
]

# Check that the spawn probabilities are correct in cleanup
# Map to check that cleanup beam removes waste correctly
CLEANUP_PROB_MAP = [
    "@@@@@@",
    "@    @",
    "@HHPB@",
    "@RH B@",
    "@H PB@",
    "@@@@@@",
]
def get_env_test_map(env):
    """Gets a version of the environment map where generic
    'P' characters have been replaced with specific agent IDs.

    Returns:
        2D array of strings representing the map.
    """
    grid = np.copy(env.world_map)

    for agent_id, agent in env.agents.items():
        # If agent is not within map, skip.
        if not (0 <= agent.pos[0] < grid.shape[0] and 0 <= agent.pos[1] < grid.shape[1]):
            continue

        grid[agent.pos[0], agent.pos[1]] = b"P"

    for beam_pos in env.beam_pos:
        grid[beam_pos[0], beam_pos[1]] = beam_pos[2]

    return grid
class DummyMapEnv(MapEnv):
    """This class implements a few missing methods in map env that are needed for testing."""

    def setup_agents(self):
        map_with_agents = self.get_map_with_agents()

        for i in range(self.num_agents):
            agent_id = "agent-" + str(i)
            spawn_point = self.spawn_point()
            rotation = self.spawn_rotation()
            grid = map_with_agents
            # grid = util.return_view(map_with_agents, spawn_point,
            #                         2, 2)
            agent = DummyAgent(agent_id, spawn_point, rotation, grid, 2, 2)
            self.agents[agent_id] = agent

    def execute_custom_reservations(self):
        return


class DummyAgent(Agent):
    def reward_from_pos(self, new_pos):
        return 0

    def get_done(self):
        return False

    def action_map(self, action_number):
        return BASE_ACTIONS[action_number]

    @property
    def action_space(self):
        return DiscreteWithDType(len(ACTION_MAP), dtype=np.uint8)

    def consume(self, char):
        return char

