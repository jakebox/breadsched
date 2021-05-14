###
### Flask Views for BreadSched
### Handles serving pages, runnning calculation off of user input
### (c) 2021 J. Boxerman
###

from flask import render_template, request, redirect
from app import app

from calculations import *


@app.route("/", methods=["GET", "POST"])
def index():
   if request.method == "GET":
      return render_template('index.html')
   else:

      times = {"mixing_time": "0", "rise0": "0",
               "action_time": "0", "rise1": "0", "bake_time": "0",
               "cool_time": "0"}

      # get bread process time information
      for key, value in times.items():
         form_data = request.form.get(key)
         if form_data != "": times[key] = int(request.form.get(key))
         else: times[key] = 0
      
      bread_kind = str(request.form.get("bread_kind"))

      # Get the first rise range, if nonexistent set equal to 0
      first_rise_range = request.form.get("first_rise_range")
      if first_rise_range == "": first_rise_range = 0
      else: first_rise_range = int(first_rise_range)

      target_time = str(request.form.get("target_time"))
      minimum_start_time = str(request.form.get("minimum_start_time"))

      bread = Bread(target_time, minimum_start_time, bread_kind, times, first_rise_range)

      try:
         bread.calculate_time()
      except ValueError:
         # display error message if necessary e.g. print str(e)
         print("Failed, error out.")
         return render_template("index.html", error="time_error")
      else:
         if target_time != "":
            target_timeJ = True
            latest_possible_start = bread.calc_lps()
            bread.calculate_schedule(latest_possible_start[0:2], latest_possible_start[3:5])
         else:
            target_timeJ = False
            latest_possible_start = twentyfour_to_twelve(minimum_start_time)
            bread.calculate_schedule(minimum_start_time[0:2], minimum_start_time[3:5])

         return render_template("output.html", target_time=target_timeJ, bread_object=bread,
                                latest_possible_start=twentyfour_to_twelve(latest_possible_start),
                                total_rise_hours=int(bread.total_rise_time / 60),
                                total_rise_mins=(bread.total_rise_time % 60))


@app.route("/output")
def output():
   if request.method == "GET":
      return render_template("error.html", error_reason="You haven't filled out any details yet!")

@app.route("/info")
def info():
   if request.method == "GET":
      return render_template("info.html")
