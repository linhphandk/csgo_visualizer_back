from ariadne import (
    gql,
    QueryType,
    make_executable_schema,
)
from ariadne.asgi import GraphQL
from fastapi import FastAPI
from src.seed.seed import seed_database
from src.services.mongo_service import get_client
from bson.json_util import dumps
from fastapi.responses import JSONResponse
from bson.json_util import dumps
import json
app = FastAPI(on_startup=[seed_database])
@app.get("/")
def resolve_actions():
    client = get_client()
    res = client.find_one("player_action")
    return JSONResponse(content=json.loads(dumps(res)))