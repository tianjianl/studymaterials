from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("welcome.html")


@app.route('/signup')
def signup():
    if request.args.get("next") == 'confirm':
        return render_template("signup.html", next=request.args.get("next"))
    else:
        return render_template("signup.html")


@app.route('/confirm')
def confirm():
    if request.args.get("next", "welcome") == 'welcome':
        return render_template("confirm.html", next=request.args.get("next", "welcome"))
    else:
        return render_template("confirm.html")

if __name__ == '__main__':
    app.run(debug=False)
