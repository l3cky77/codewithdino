from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("codewithdino.html")


@app.route("/course")
def course():
    return render_template("courses.html")


@app.route("/home")
def about():
    return render_template("codewithdino.html")


@app.route("/roadmap")
def roadmap():
    return render_template("roadmap.html")


@app.route("/aibot")
def aibot():
    return render_template("dinoai.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
