from flask import render_template, request, redirect, url_for, flash
from app import app

from calculations import *


@app.route("/", methods=["GET", "POST"])
def index():
   if request.method == "GET":
      return render_template('index.html')
   else:
      # TODO - compact this/optimize
      bread_kind = str(request.form.get("bread_kind"))
      mixtime = int(request.form.get("mixtime"))
      first_rise = int(request.form.get("first_rise"))
      first_rise_range = int(request.form.get("first_rise_range"))
      second_rise = int(request.form.get("second_rise"))
      action_time = int(request.form.get("action_time"))
      bake_time = int(request.form.get("bake_time"))
      cool_time = int(request.form.get("cool_time"))
      target_time = str(request.form.get("target_time"))
      minimum_start_time = str(request.form.get("minimum_start_time"))

      times = {"mixing_time": mixtime, "rise0": first_rise,
               "action_time": action_time, "rise1": second_rise, "bake_time": bake_time,
               "cool_time": cool_time}

      bread = Bread(target_time, minimum_start_time, "Challah", times, first_rise_range)

      try:
         bread.calculate_time()
      except ValueError:
         # display error message if necessary e.g. print str(e)
         print("Failed, error out.")
         return render_template("index.html", error="time_error")
      else:
         print("Original first rise:", first_rise, "| Adjusted first rise:", bread.times.get('rise0'))

         if target_time != "":
            print("We've got a target time")
            latest_possible_start = bread.calc_lps()
            bread.calculate_schedule(latest_possible_start[0:2], latest_possible_start[3:5])
            return render_template("output.html", target_time=True, bread_object=bread, latest_possible_start=twentyfour_to_twelve(latest_possible_start), total_rise_hours=int(bread.total_rise_time / 60), total_rise_mins=(bread.total_rise_time % 60))
         else:
            print("No target time, just a start time")
            bread.calculate_schedule(minimum_start_time[0:2], minimum_start_time[3:5])
            return render_template("output.html", target_time=False, bread_object=bread, latest_possible_start=twentyfour_to_twelve(minimum_start_time), total_rise_hours=int(bread.total_rise_time / 60), total_rise_mins=(bread.total_rise_time % 60))


@app.route("/output")
def output():
   if request.method == "GET":
      return render_template("error.html", error_reason="You haven't filled out any details yet!")
