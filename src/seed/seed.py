"""
contains scripts that
are used on startup
"""
from pathlib import Path

from services.mongo_service import get_client
from parsers.get_match_data import get_game_data
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
        print(client.list_collection_names())
        data = get_game_data(Path('./src/assets/data.txt'))
        client.insert_many([d.serialize() for d in data], 'player_action')
