from flask import render_template, request, redirect, url_for
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
      second_rise_range = int(request.form.get("second_rise_range"))
      action_time = int(request.form.get("action_time"))
      bake_time = int(request.form.get("bake_time"))
      cool_time = int(request.form.get("cool_time"))
      target_time = str(request.form.get("target_time"))
      minimum_start_time = str(request.form.get("minimum_start_time"))

      bread = Bread(target_time, minimum_start_time, bread_kind, mixtime, first_rise, first_rise_range, second_rise, second_rise_range, action_time, bake_time, cool_time)

      bread.calculate_time(False)
      latest_possible_start = bread.calc_lps()
      bread.calculate_schedule(latest_possible_start[0:2], latest_possible_start[3:5])

      # return redirect("/output") # Send to output page
      # return redirect(url_for('output', user=user_name))
      return render_template("output.html", user="Jake", bread_object=bread, time_target=twentyfour_to_twelve(target_time), latest_possible_start=twentyfour_to_twelve(latest_possible_start), bread_kind=bread.bread_kind, total_rise_time=int(bread.total_rise_time/60 * 100) / 100)

@app.route("/output")
def output():
   if request.method == "GET":
      # return render_template("output.html", bread="")
      # return render_template("error.html")
      return render_template("error.html", error_reason="You haven't filled out any details yet!")
