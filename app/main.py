import os,demo

from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/<int:sDate>/<int:fr>/<keyW>')
def hello_world(sDate,fr,keyW):
    try:
        sttr = demo.main2(sDate,fr,keyW)
        return jsonify(sttr)
    except Exception as e:
        zz = str(e)
        aa = zz + "okkkkkkkkkkkkkktt"
        return aa



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

