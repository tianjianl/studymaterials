from flask import Flask, render_template
from flask import request
from flask_csp.csp import csp_header

app = Flask(__name__)

@app.route('/')
@csp_header({
    'script-src':"'self' 'nonce-pizza' 'unsafe-hashes' 'sha256-KBtTth8y8zW7frEwgE4qj0scUERBLG3xjeSHSwLdRhs=' 'sha256-3KEnLNXB6XGg3A2Mz7TZ5eSwKIgts7/Sos89qK1AAQU=' ",
})
def level4():
    if request.method == 'GET':
        if not request.args.get('timer'):
            return render_template('index4.html')
        else:
            timer = request.args.get('timer')
            return render_template("timer.html", timer=timer)


@app.route('/csp_report', methods=['POST'])
def csp_report():
	with open('./csp_report', "a") as fh:
		fh.write(request.data.decode() + '\n')
	return 'done'

if __name__ == '__main__':
    app.run(debug=False)
