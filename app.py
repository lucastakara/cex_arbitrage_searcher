from flask import Flask, render_template, jsonify
from cex_arb.arb_searcher import ArbSearcher

app = Flask(__name__)


@app.route("/get_opportunities", methods=['GET'])
def get_opportunities_data():
    arb_searcher = ArbSearcher()
    opportunities = arb_searcher.get_opportunities(100)
    return jsonify(opportunities)


@app.route("/", methods=["GET"])
def index():
    return render_template("opportunity_table.html")


if __name__ == "__main__":
    app.run(debug=True)
