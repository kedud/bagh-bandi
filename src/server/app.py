import sys, os

sys.path.insert(0, os.getcwd())

from flask import Flask
from src.domain.engine import Engine
from src.agents.minimax import MinimaxABAgent
import json

app = Flask(__name__)

engine = Engine()

agent = None

@app.route('/state', methods=['GET', 'POST'])
def state():
    ret = {}
    ret["goat_positions"] = engine.board.goatsPositions
    ret["tigers_positions"] = engine.board.tigerPositions
    ret["turn"] = engine.board.turn
    ret["re_capture_allowed"] = engine.re_capture_allowed
    return json.dumps(ret)


@app.route('/move/<player_type>/<int:departure>/<int:destination>', methods=['GET', 'POST'])
def postId(player_type, departure, destination):
    global agent, engine
    if player_type == engine.board.turn:
        if engine.is_valid_move(departure, destination, engine.board):
            engine.board = engine.move(departure, destination, engine.board)
            if agent and engine.board.turn != player_type:
                agent.moves()
            return "OK"
        else:
            return (f"/!\\ INVALID MOVE : {departure} to {destination}")
    else:
        return "NOT YOUR TURN"


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    global engine
    engine = Engine()
    return "OK"


@app.route('/skip/<player_type>', methods=['GET', 'POST'])
def skip_turn(player_type):
    global engine
    if engine.re_capture_allowed and engine.board.turn == player_type and player_type == "tigers":
        engine.skip_tiger_recapture()
        if agent and engine.board.turn != player_type:
            agent.moves()
        return "OK"
    else:
        return "Cannot skip turn"


@app.route('/setup_agent/<agent_type>', methods=['GET', 'POST'])
def setup_agent(agent_type):
    global agent
    agent = MinimaxABAgent(agent_type, engine)
    return "agent setup OK"

@app.route('/move_agent', methods=['GET', 'POST'])
def move_agent():
    global agent
    agent.moves()


def main():
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
