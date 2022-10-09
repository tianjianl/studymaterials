from flask import Flask, render_template, request
from flask_csp.csp import csp_header 
from flask import redirect, url_for
app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('welcome'))

@app.route('/welcome')
@csp_header({
    'script-src':"'self'",
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
    'script-src':"'self'"
})
def confirm():
    return render_template("confirm.html", next=request.args.get("next", "welcome"))


@app.route('/csp_report', methods=['POST'])
def csp_report():
	with open('./csp_report', "a") as fh:
		fh.write(request.data.decode() + '\n')
	return 'done'


if __name__ == '__main__':
    app.run(debug=False)
