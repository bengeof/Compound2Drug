from flask import Flask
from infer import * 

app = Flask(__name__)

# "/cid" endpoint that returns the list of structurally related pdbids for the givewn cid
@app.route("/<cid>", methods=["GET"])
def main(cid):
    return predict(str(cid))

if __name__ == "__main__":
    app.run(debug=True)
