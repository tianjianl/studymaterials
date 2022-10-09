from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def level3():
    return render_template("index3.html")
if __name__ == '__main__':
    app.run(debug=False)
