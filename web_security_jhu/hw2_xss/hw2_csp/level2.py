from flask import Flask, request, render_template
from flask_csp.csp import csp_header

app = Flask(__name__)

@app.route('/')
@csp_header({
    'script-src':"'self'",
    'img-src':"'self' ssl.gstatic.com"
})
def level2():
    return render_template("index2.html")


@app.route('/csp_report', methods=['POST'])
def csp_report():
	with open('./csp_report', "a") as fh:
		fh.write(request.data.decode() + '\n')
	return 'done'

if __name__ == '__main__':
    app.run(debug=False)
