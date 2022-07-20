from analyse import analyse
from flask import Flask, request
from flask import jsonify
app = Flask(__name__)


@app.route('/analyse')
def index():

    text = request.args.get('input')
    return jsonify(analyse(text))

if __name__ == "__main__":
    app.run("0.0.0.0", port=4030, debug=True)
    # from waitress import serve