from flask import Flask, request, redirect, url_for, render_template, jsonify
import re


page_header = """<!doctype html>
<html>
  <head>
    <!-- Internal game scripts/styles, mostly boring stuff -->
    <script src="/static/game-frame.js"></script>
    <link rel="stylesheet" href="/static/game-frame-styles.css" />
  </head>

  <body id="level1">
    <img src="/static/logos/level1.png">
      <div>
"""

page_footer = """
    </div>
  </body>
</html>
"""

main_page_markup = """
<form action="" method="GET">
  <input id="query" name="query" value="Enter query here..."
    onfocus="this.value=''">
  <input id="button" type="submit" value="Search">
</form>
"""

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for("level"))


@app.route('/level1/frame')
def level():
    if request.method == 'GET':
        query = request.args.get('query')
        if not query:
            content = page_header + main_page_markup + page_footer

            pagefile = open("templates/level1_index.html", "w")
            pagefile.write(content)
            pagefile.close()
            return render_template("level1_index.html")
        else:
            query = re.sub(r'</?\w+[^>]*>', '', query)

            message = "Sorry, no results were found for <b>" + query + "</b>."
            message += " <a href='?'>Try again</a>."
            content = page_header + message + page_footer

            pagefile = open("templates/level1_result.html", "w")
            pagefile.write(content)
            pagefile.close()
            return render_template("level1_result.html")


if __name__ == '__main__':
    app.run(debug=False)
