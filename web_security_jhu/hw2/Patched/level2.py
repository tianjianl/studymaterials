from flask import Flask, request, redirect, url_for, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for("level"))


@app.route('/level2/frame')
def level():
    return render_template("level2_index.html")


if __name__ == '__main__':
    app.run(debug=False)
