from flask import request, session, jsonify
from game_numpy_serializable import GameSerializable
from logic.minmax import find_best_move
from flask import Flask, render_template

app = Flask(__name__, static_folder="static", template_folder="static/template", static_url_path='/')

app.secret_key = b'jeefqdqdcqdqsdqsd'


@app.route('/')
def home():
    session.clear()
    return render_template('index.html')


@app.route('/best_move', methods=['POST'])
def best_move():
    data = request.get_json()
    print(session.get("game", None))
    game = session.get("game", None)
    if game is None:
        game = GameSerializable(3, 3)
    else:
        game = GameSerializable.from_dict(game)
    last_move = int(data['last_play'])
    game.play(last_move, player=-1)
    best_move = find_best_move(game)
    game.play(best_move, player=1)
    session["game"] = game.to_dict()

    return jsonify({'best_move': int(best_move)})


if __name__ == "__main__":
    app.run(debug=True)
