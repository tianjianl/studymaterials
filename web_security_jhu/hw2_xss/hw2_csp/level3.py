from flask import Flask, request, render_template
from flask_csp.csp import csp_header

app = Flask(__name__)

@app.route('/')
@csp_header({
    'script-src':"'self' 'unsafe-hashes' 'sha256-AnDVymxFQ3SNPFvGTp6Xbh2Cef+9yLo4n/nJAMA7daI=' 'sha256-5GwV0JsBobqZcbVCKSlLFeHE0He4GTeXJrc+b6OOEGs=' 'sha256-rEl3vo2eeGsIK5QdBfnVWMffvMkYoFv/HHBRwsnkBgg=' ajax.googleapis.com",
})
def level3():
    return render_template("index3.html")
@app.route('/csp_report', methods=['POST'])
def csp_report():
	with open('./csp_report', "a") as fh:
		fh.write(request.data.decode() + '\n')
	return 'done'


if __name__ == '__main__':
    app.run(debug=False)
