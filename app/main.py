import os

from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/<int:sDate>/<int:fr>/<keyW>')
def hello_world(sDate,fr,keyW):
    try:
        import search
        gettt = search.askURL(1, 0, "本科")
        gettt=str(gettt)
        return gettt
    except Exception as e:
        return str(e)+"error"


if __name__ == "__main__":
    app.run(debug=True)
