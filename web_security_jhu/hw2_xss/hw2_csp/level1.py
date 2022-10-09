from flask import Flask, request, render_template
from flask_csp.csp import csp_header

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
@csp_header({
    'script_src':"'self'"
})
def level1():
    if request.method == 'GET':
        query = request.args.get('query')
        if not query:
            content = page_header + main_page_markup + page_footer
            template = open("templates/index1.html", "w")
            template.write(content)

            template.close()
            return render_template("index1.html")
        else:
            message = "Sorry, no results were found for <b>" + query + "</b>."
            message += " <a href='?'>Try again</a>."
            content = page_header + message + page_footer

            template = open("templates/result1.html", "w")
            template.write(content)
            template.close()
            return render_template("result1.html")

if __name__ == '__main__':
    app.run(debug=True)
