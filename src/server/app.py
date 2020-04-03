from flask import Flask
from src.domain.engine import Engine
import json

app = Flask(__name__)

engine = Engine()

@app.route('/state', methods=['GET', 'POST'])
def state():
    ret = {}
    ret["goat_positions"] = engine.board.goatsPositions
    ret["tigers_positions"] = engine.board.tigerPositions
    ret["turn"] = engine.board.turn
    return json.dumps(ret)

@app.route('/move/<player_type>/<int:departure>/<int:destination>', methods=['GET', 'POST'])
def postId(player_type, departure, destination):
    if player_type == engine.board.turn:
        if engine.is_valid_move(departure, destination):
            engine.move(departure, destination)
            return "OK"
        else:
            return(f"/!\\ INVALID MOVE : {departure} to {destination}")
    else:
        return "NOT YOUR TURN"


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    global engine
    engine = Engine()
    return "OK"


@app.route('/', methods=['GET', 'POST'])
def lol():
    return "PAS DANS LE NAVIGATEUR DEBILOS"