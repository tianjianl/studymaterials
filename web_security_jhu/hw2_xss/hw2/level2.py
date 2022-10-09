from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def level2():
    return render_template("index2.html")


if __name__ == '__main__':
    app.run(debug=False)
