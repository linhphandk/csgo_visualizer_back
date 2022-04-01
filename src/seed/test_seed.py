"""
seeding tests
"""
from unittest import TestCase
from pathlib import Path

from services.mongo_service import get_client
from parsers.get_match_data import get_game_data
from .seed import seed_database
class TestSeedData(TestCase):
    """
    seed data test suite
    """
    def setUp(self):
        self.path = Path('./src/assets/data.txt')
        self.client = get_client()

    def test_db_seed(self):
        """
        seed test
        """
        seed_database()
        data = get_game_data(self.path)
        self.client.insert_many([d.serialize() for d in data], 'player_action')
    