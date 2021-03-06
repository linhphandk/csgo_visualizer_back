from fastapi import FastAPI
from src.seed.seed import seed_database
from src.services.mongo_service import get_client
from bson.json_util import dumps
from fastapi.responses import JSONResponse
from bson.json_util import dumps
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(on_startup=[seed_database])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def resolve_actions():
    client = get_client()
    actions = client.find("player_action")
    teams = client.find("teams")
    data = {
        "rounds": actions,
        "teams": teams
    }
    return JSONResponse(content=json.loads(dumps(data)))
