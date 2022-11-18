from globals import app
from flask import render_template
from src.search import Searcher


@app.route("/")
@app.route("/index")
def index_route():
    return render_template("main.html")


@app.route("/search/tfidf/")
@app.route("/search/tfidf/<string:request>")
def search_tfidf_route(request: str = ""):
    if not request:
        results = None
    else:
        results = Searcher.get_tfidf_results(request)
    return render_template(
        "results.html",
        method="search_tfidf_route",
        request=request,
        results=results,
        show_requests=True
    )


@app.route("/search/lsa/")
@app.route("/search/lsa/<string:request>")
def search_lsa_route(request: str = ""):
    if not request:
        results = None
    else:
        results = Searcher.get_lsa_results(request)
    return render_template(
        "results.html",
        method="search_lsa_route",
        request=request,
        results=results,
        show_requests=True,
        can_be_slow=True
    )


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5555)
