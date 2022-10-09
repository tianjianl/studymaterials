from flask import Flask, render_template
from flask import redirect, url_for
app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('level6'))

@app.route('/level6/frame')
def level6():
    return render_template("index6.html")


if __name__ == '__main__':
    app.run(debug=True)
