"""
contains scripts that
are used on startup
"""
from pathlib import Path

from src.services.mongo_service import get_client
from src.parsers.get_match_data import get_game_data
def seed_database():
    """
    function used for seeding data
    on startup
    """
    client = get_client()
    col_name = 'player_action'
    if col_name in client.list_collection_names():
        print("already seeded")
    else:
        data = get_game_data(Path('./src/assets/data.txt'))
        client.insert_many([d.serialize() for d in data["round_list"]], 'player_action')
        client.insert( data['teams'], 'teams')
