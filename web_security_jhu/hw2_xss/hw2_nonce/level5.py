from flask import Flask, render_template, request, redirect, url_for
from flask_csp.csp import csp_header 
app = Flask(__name__)

@app.route('/')
def level5():
    return redirect(url_for('welcome'))

@app.route('/welcome')
@csp_header({
    'script-src':"'self'"
})
def welcome():
    return render_template("welcome.html")


@app.route('/signup')
@csp_header({
    'script-src':"'self'"
})
def signup():
    return render_template("signup.html", next=request.args.get("next"))


@app.route('/confirm')
@csp_header({
    'script-src':"'self' 'nonce-pizza'"
})
def confirm():
    return render_template("confirm.html", next=request.args.get("next", "welcome"))

if __name__ == '__main__':
    app.run(debug=False)
