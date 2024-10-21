import json
from helpers.db import db
from flask import Flask, request
from loguru import logger

app = Flask(__name__)

HISTORY_LENGTH = 10
DATA_KEY = "engine_temperature"

@app.route('/record', methods=['POST'])
def record_engine_temperature():
    payload = request.get_json(force=True)
    logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

    engine_temperature = payload.get("engine_temperature")
    logger.info(f"engine temperature to record is: {engine_temperature}")

    db.lpush(DATA_KEY, engine_temperature)
    logger.info(f"stashed engine temperature in redis: {engine_temperature}")

    while db.llen(DATA_KEY) > HISTORY_LENGTH:
        db.rpop(DATA_KEY)
    engine_temperature_values = db.lrange(DATA_KEY, 0, -1)
    logger.info(f"engine temperature list now contains these values: {engine_temperature_values}")

    logger.info(f"record request successful")
    return {"success": True}, 200

@app.route('/collect', methods=['POST'])
def collect_engine_temperature():
    return {"success": True}, 200