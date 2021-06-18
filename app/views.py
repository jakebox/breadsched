###
### Flask Views for BreadSched
### Handles serving pages, runnning calculation off of user input
### (c) 2021 J. Boxerman
###

from flask import render_template, request, redirect
from app import app

from calculations import *


@app.route("/")
def index():
   if request.method == "GET":
      return render_template("index.html")


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
   if request.method == "GET":
      return render_template('calculator.html')
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
      if bread_kind == "": bread_kind = "Unspecified bread"

      # Get the first rise range, if nonexistent set equal to 0
      first_rise_range = request.form.get("first_rise_range")
      if first_rise_range == "": first_rise_range = 0
      else: first_rise_range = int(first_rise_range)

      target_time = str(request.form.get("target_time"))
      minimum_start_time = str(request.form.get("minimum_start_time"))
      if (len(minimum_start_time) != 5): minimum_start_time = "0" + minimum_start_time # Add a leading zero to the time if needed
      print(minimum_start_time)
         

      bread = Bread(target_time, minimum_start_time, bread_kind, times, first_rise_range)

      try:
         bread.calculate_time()
      except ValueError: # display error message if necessary e.g. print str(e)
         print("Failed, error out.")
         return render_template("calculator.html", error="time_error")
      else: # If there is no error
         if target_time != "": # Target time, so start as late as possible
            target_timeJ = True
            latest_possible_start = bread.calc_lps()
            bread.calculate_schedule(latest_possible_start[0:2], latest_possible_start[3:5])
         else: # No target time, so just use the LPS as the start time
            target_timeJ = False
            # This LPS isn't actually used, it's just for visual purposes, really it's just the desired start time
            latest_possible_start = minimum_start_time[0:2] + ":" + minimum_start_time[3:5] 
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

@app.route("/help")
def help():
   if request.method == "GET":
      return render_template("help.html")

@app.route("/testing", methods=["GET", "POST"])
def testing():
   if request.method == "GET":
      return render_template("testing.html")
   else:
      time = str(request.form.get("time0"))
      print(time)
      
