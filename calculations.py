from datetime import datetime, timedelta

class Bread():

    def __init__(self, time_target, minimum_start_time, bread_kind, mixtime, rise0, rise0_range, rise1, rise1_range, action_time, bake_time, cool_time):

        # User-provided values
        self.bread_kind = bread_kind

        # How much to change the times by if you are too close on time (WIP WILL CHANGE)
        self.reduction_factor = 0.2

        # Dict of times
        self.times = {"mixing_time": mixtime, "rise0": rise0,
                      "action_time": action_time, "rise1": rise1, "bake_time": bake_time,
                      "cool_time": cool_time}

        # Dict for the two time ranges
        self.time_ranges = {"rise0_range": rise0_range, "rise1_range": rise1_range}

        # Clock times
        self.time_target_full = time_target
        self.time_target = time_target.replace(':', '')
        self.time_target_hours = int(self.time_target[0:2])
        self.time_target_minutes = int(self.time_target[2:4])
        self.minimum_start_time = minimum_start_time.replace(':', '')

        # Initializing calculated values
        self.total_rise_time = 0
        self.available_baking_time = 0

        # First thing to do is calculate how many minutes you have available to you
        # (time between earliest possible start and target time)
        self.calc_available_baking_time()


    def calc_available_baking_time(self):
        """ Calculate how many hours you have to get your bread done.
        Assumes you can start at minimum_start_time and you must be
        done at time_target """

        a = timedelta(hours=self.time_target_hours, minutes=self.time_target_minutes)
        b = timedelta(hours=int(self.minimum_start_time[0:2]), minutes=int(self.minimum_start_time[2:4]))
        datetime_obj = a - b
        self.available_baking_time = datetime_obj.seconds / 60 # Available baking time in hours


    def calculate_time(self, rerun_shorter=False):
    # Total process time comes out in minutes
        if not rerun_shorter:
            for time in self.times.values():
                self.total_rise_time = self.total_rise_time + time # Summing the times
            if (self.total_rise_time > self.available_baking_time): # +10 for a bit of room
                print("Rise time greater than baking time")
                print("Naive total rise time:", self.total_rise_time)
                self.calculate_time(True) # Rerun the calculations but with a time reduction
            else:
                return 0 # Time successfully calculated
        else: # If we are recalculating the time:
            print("Got to else")
            self.total_rise_time = 0 # Reset the time

            time_wo_rise0 = 0
            for label, time in self.times.items():
                if label == "rise0":
                    pass
                else:
                    time_wo_rise0 += time
            # minimum rise 0 + rest of time < total time, we're good
            if (self.times.get('rise0') - self.time_ranges.get('rise0_range') + time_wo_rise0 <= self.available_baking_time):
                print("It is possible to make your bread!")
                # x = self.times.get('rise0') - self.time_ranges.get('rise0_range') + time_wo_rise0
                rise_offset = -1 * self.available_baking_time + time_wo_rise0 + self.times.get('rise0')
                # print(rise_offset)
                self.times['rise0'] -= rise_offset # Adjusted rise0
                # print(self.times['rise0'])
                self.calculate_time()
            else:
                # Ends here
                raise ValueError("Not enough time to make the bread.")


    def calc_lps(self):
        # Calculate a latest possible time to start the bread. Returns in 24 hour time.
        latest_possible_start = timedelta()
        latest_possible_start = timedelta(hours=self.time_target_hours, minutes=self.time_target_minutes) - timedelta(hours=(self.total_rise_time / 60))
        dp = str(latest_possible_start)[:-3] # Return the time but without the seconds bit (so just HH:MM)
        return dp

    def calculate_schedule(self, hours, minutes):
        # Takes in a starting time as hours and minutes (24-hour) and
        # loops thru each time amount, setting the time in a dict along the way
        self.rise0_end = ''
        self.rise1_end = ''
        
        start_time = timedelta(hours=int(hours), minutes=int(minutes))
        current_time = start_time
        self.schedule = self.times.copy() # Make a copy of the timetable to refer to and to store the schedule
        self.schedule = {key:val for key, val in self.schedule.items() if val != 0} # Remove items that take no time (val=0)
        self.schedule['eat'] = 0 # So eating is on the schedule after cooling

        for key, time in self.schedule.items():
            # Set the value of the key to a 12-hour string version (i.e 12:50 PM) of the 'current'
            # time, which is the time the event should begin, then increment the counter by the amount of timedelta
            # that was used. I think this only works because there is a copy being made somewhere but I'm not sure.
            self.schedule[key] = twentyfour_to_twelve(str(current_time)[:-3])
            current_time += timedelta(minutes=time)
            if key == 'rise0':
                self.rise0_end = twentyfour_to_twelve(str(current_time)[:-3])
            elif key == 'rise1':
                self.rise1_end = twentyfour_to_twelve(str(current_time)[:-3])
        


def twentyfour_to_twelve(time):
    # Convert a 24-hour string to a 12-hour string + AM/PM
    # ex: (18:00 -> 6:00 PM)
    d = datetime.strptime(time, "%H:%M")
    return str(d.strftime("%I:%M %p"))
    

if __name__ == '__main__':

    minimum_start_time = "10:00"
    time_target = "18:30"

    mixtime = 30
    first_rise = 180
    first_rise_range = 30
    second_rise = 60
    second_rise_range = 30
    action_time = 15
    bake_time = 35
    cool_time = 15

    bread = Bread(time_target, minimum_start_time, "Challah", mixtime, first_rise, first_rise_range, second_rise, second_rise_range, action_time, bake_time, cool_time)

    try:
        bread.calculate_time()
    except ValueError:
    # display error message if necessary e.g. print str(e)
        print("Failed, error out.")
    else:
        latest_possible_start = bread.calc_lps()

        # Could be done using any times - so if you don't have a target time but you do have a start time this could be used
        bread.calculate_schedule(latest_possible_start[0:2], latest_possible_start[3:5])

        print("\nAvailable baking time:", bread.available_baking_time, "| Total process time:", bread.total_rise_time)
        print("Original first rise:", first_rise, "| Adjusted first rise:", bread.times.get('rise0'))
        print("\nYour", bread.bread_kind, "will take", bread.total_rise_time, "minutes total, equal to", "{:.2f}".format((bread.total_rise_time/60)), "hours.\n The latest you could possibly start at to make it on time for", twentyfour_to_twelve(bread.time_target_full), "is", twentyfour_to_twelve(latest_possible_start))
        print("\nSCHEDULE:")
        for key, value in bread.schedule.items():
            print(key.capitalize() + ":", value)
        
