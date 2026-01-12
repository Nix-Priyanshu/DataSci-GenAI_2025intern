from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    matches = []
    error = None
    no_match = False

    if request.method == "POST":
        test_string = request.form.get("test_string")
        regex = request.form.get("regex")

        try:
            matches = re.findall(regex, test_string)
        except re.error as e:
            error = str(e)

    return  render_template(
        "index.html",
        matches=matches,
        error=error,
        no_match=no_match
        )

if __name__ == "__main__":
    app.run(debug=True)
