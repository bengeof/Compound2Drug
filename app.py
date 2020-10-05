from flask import Flask
from infer import * 

app = Flask(__name__)

@app.route("/<cid>", methods=["GET"])
def main(cid):
    return predict(str(cid))

if __name__ == "__main__":
    app.run(debug=True)
