from flask import Flask, render_template, request
from flask import redirect, url_for
from flask_csp.csp import csp_header 
app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('level6'))

@app.route('/level6/frame')
@csp_header({
    'script-src':"'self' 'nonce-pizza'"
})
def level6():
    return render_template("index6.html")


@app.route('/csp_report', methods=['POST'])
def csp_report():
	with open('./csp_report', "a") as fh:
		fh.write(request.data.decode() + '\n')
	return 'done'


if __name__ == '__main__':
    app.run(debug=True)
