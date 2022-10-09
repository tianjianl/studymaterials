from flask import Flask, render_template
from flask import request

app = Flask(__name__)
@app.route('/')
def level():
    if request.method == 'GET':
        if not request.args.get('timer'):
            return render_template('index4.html')
        else:
            timer = request.args.get('timer')
            for s in timer:
                if s not in ['0','1','2','3', '4', '5', '6', '7', '8', '9']:
                    timer = '5'
                    break

            return render_template("timer.html", timer=timer)

if __name__ == '__main__':
    app.run(debug=False)
