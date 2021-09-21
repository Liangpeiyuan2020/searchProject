import os

from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/<int:sDate>/<int:fr>/<keyW>')
def hello_world(sDate,fr,keyW):
    try:
        import search
        return jsonify(search.askURL(sDate,fr,keyW))
    except Exception as e:
        return str(e)+"error"


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
