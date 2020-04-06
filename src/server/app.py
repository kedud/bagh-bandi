import sys, os
sys.path.insert(0, os.getcwd())

from flask import Flask, send_from_directory, render_template
from src.domain.engine import Engine
import json
import flask

app = Flask(__name__, static_url_path='')

engine = Engine()

@app.route('/')
def root():
    return app.send_static_file("index.html")

@app.route('/state', methods=['GET', 'POST', 'OPTIONS'])
def state():
    ret = {}
    ret["goat_positions"] = engine.board.goatsPositions
    ret["tigers_positions"] = engine.board.tigerPositions
    ret["turn"] = engine.board.turn
    ret["re_capture_allowed"] = engine.re_capture_allowed

    response = flask.jsonify(ret)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response


@app.route('/move/<player_type>/<int:departure>/<int:destination>', methods=['GET', 'POST'])
def postId(player_type, departure, destination):
    msg = "OK"
    if player_type == engine.board.turn:
        if engine.is_valid_move(departure, destination):
            engine.move(departure, destination)
        else:
            msg = f"/!\\ INVALID MOVE : {departure} to {destination}"
    else:
        msg = "NOT YOUR TURN"

    ret = {}
    ret["msg"] = msg
    ret["goat_positions"] = engine.board.goatsPositions
    ret["tigers_positions"] = engine.board.tigerPositions
    ret["turn"] = engine.board.turn
    ret["re_capture_allowed"] = engine.re_capture_allowed
    response = flask.jsonify(ret)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response



@app.route('/reset', methods=['GET', 'POST'])
def reset():
    global engine
    engine = Engine()

    msg = "OK"

    ret = {}
    ret["msg"] = msg
    ret["goat_positions"] = engine.board.goatsPositions
    ret["tigers_positions"] = engine.board.tigerPositions
    ret["turn"] = engine.board.turn
    ret["re_capture_allowed"] = engine.re_capture_allowed
    response = flask.jsonify(ret)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response



@app.route('/skip/<player_type>', methods=['GET', 'POST'])
def skip_turn(player_type):
    global engine
    msg = "OK"
    if engine.re_capture_allowed and engine.board.turn == player_type and player_type == "tigers":
        engine.skip_tiger_recapture()
        msg = "OK"
    else:
        msg = "Cannot skip turn"

    ret = {}
    ret["msg"] = msg
    ret["goat_positions"] = engine.board.goatsPositions
    ret["tigers_positions"] = engine.board.tigerPositions
    ret["turn"] = engine.board.turn
    ret["re_capture_allowed"] = engine.re_capture_allowed
    response = flask.jsonify(ret)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response

def main():
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
