from flask import request, session, jsonify
from game_numpy_serializable import GameSerializable
from logic.minmax import find_best_move
from flask import Flask, render_template

app = Flask(__name__, static_folder="static", template_folder="static/template", static_url_path='/')

app.secret_key = b'jeefqdqdcqdqsdqsd'
HISTORY_PATH = "history.txt"


@app.route('/')
def home():
    session.clear()
    return render_template('index.html')


@app.route('/best_move', methods=['POST'])
def best_move():
    data = request.get_json()
    game = session.get("game", None)
    if game is None:
        game = GameSerializable(3, 3)
    else:
        game = GameSerializable.from_dict(game)
    last_move = int(data['last_play'])
    game.play(last_move, player=-1)
    best_move, valuations = find_best_move(game)
    game.play(best_move, player=1)
    session["game"] = game.to_dict()
    print(valuations)
    return jsonify({'best_move': int(best_move), 'valuations': valuations})


@app.route('/save_history', methods=['POST'])
def save_history():
    data = request.get_json()
    history = data.get("history", None)
    observation = data.get("observation","No observation")
    str_to_write = ', '.join(map(str, history))
    with open(HISTORY_PATH, 'a') as f:
        f.write(observation + '\n')
        f.write(str_to_write + '\n')


    return jsonify({'message': 'History saved successfully'}), 200


if __name__ == "__main__":
    app.run(debug=True)
