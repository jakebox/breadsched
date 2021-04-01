from datetime import datetime
import math


class Bread():

    def __init__(self, time_target, minimum_start_hour, bread, mixtime, rise0, rise0_range, rise1, rise1_range, action_time, bake_time, cool_time):

        # User-provided values
        self.bread = bread

        self.mixing_time = mixtime
        self.rise0 = rise0
        self.rise0_range = rise0_range 
        self.rise1 = rise1
        self.rise1_range = rise1_range
        self.action_time = action_time
        self.bake_time = bake_time
        self.cool_time = cool_time

        # List of all times
        self.times = [self.mixing_time, self.rise0, self.rise1, self.action_time, self.bake_time, self.cool_time]

        # Hour-times
        self.time_target = time_target
        self.minimum_start_hour = minimum_start_hour

        # Calculated values
        self.total_rise_time = 0

    def calculate_time(self):
        for time in self.times:
            self.total_rise_time = self.total_rise_time + time

minimum_start_hour = "10am"
time_target = "5pm"

if __name__ == 'main':

    bread = Bread(time_target, minimum_start_hour, "Challah", 30, 120, 60, 60, 30, 15, 35, 15)

    bread.calculate_time()

    print("Your", bread.bread, "will take", bread.total_rise_time, "minutes total, equal to", "{:.2f}".format((bread.total_rise_time/60)), "hours.")
