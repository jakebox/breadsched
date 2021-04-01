from flask import render_template, request
from app import app

from calculations import Bread

minimum_start_hour = "10am"
time_target = "5pm"

bread = Bread(time_target, minimum_start_hour, "Brioche", 30, 120, 60, 60, 30, 15, 35, 15)


# @app.route('/index', methods = ['POST', 'GET'])

@app.route("/")
def index():
   return render_template("index.html")
   # if request.method == "POST":
   #    name = request.form['name']
   #    print("post bro")
   #    return render_template('output.html')
   # else:
   #    # userp = request.form('name')
   #    # print(userp)
   #    print("nothing in form, showing the website.")
   #    return render_template('index.html')

# , methods = ['POST', 'GET'])
@app.route("/output")
def output():
    name = request.args.get("name")
    if not name: # If no name send error page
       return render_template('error.html')
    return render_template('output.html', user=name)
