import statistics
import copy
from itertools import combinations
import numpy as np
import pandas as pd

DAYS_PER_WEEK = 7
DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class Person:
    def __init__(self, name, avail_mask: np.ndarray, time_slots=1):
        self.name = name
        # If avail mask is 1d, wrap it in a list and convrt to numpy array
        if len(avail_mask.shape) == 1:
            avail_mask = np.array([avail_mask])
        self.avail_mask = avail_mask # What times this person is available
        self.working_days = [[0] * DAYS_PER_WEEK] * time_slots  # What days this person is working on

    def can_work(self, day, time_idx=0):
        return self.avail_mask[time_idx][day]
    
    def num_shifts_worked(self):
        return sum(sum(day) for day in self.working_days)

    def assign_shift(self, day, time_idx=0):
        self.working_days[time_idx][day] = 1

    def unassign_shift(self, day, time_idx=0):
        self.working_days[time_idx][day] = 0

    def __repr__(self) -> str:
        return f"{self.name}: {self.working_days}"


class Schedule:
    def __init__(self, people, min_people_per_slot):
        self.people = people
        self.min_people_per_slot = min_people_per_slot
        self.time_slots = len(people[0].working_days) if people else 0
        self.days = DAYS_PER_WEEK

    def all_slots_worked(self, min_people_night):
        # Check if all the shifts have been worked the minimum number of times
        for day in range(self.days):
            for time_idx in range(self.time_slots):
                if sum(person.working_days[time_idx][day] for person in self.people) < min_people_night:
                    return False
        return True

    def get_balance(self):
        shifts_worked = [person.num_shifts_worked() for person in self.people]
        return statistics.stdev(shifts_worked) if shifts_worked else 0

    def assign_shifts(self, balanced_schedules, idx=0, top=10):
        if idx >= self.days * self.time_slots:
            if self.all_slots_worked(self.min_people_per_slot):
                balanced_schedules.append(copy.deepcopy(self))
                balanced_schedules.sort(key=lambda x: x.get_balance())

                if len(balanced_schedules) > top:
                    balanced_schedules.pop()
            return

        schedule_copy = copy.deepcopy(self)

        day = idx // self.time_slots
        time_idx = idx % self.time_slots

        # Get the people who can work on this day
        people_available = [person for person in schedule_copy.people if person.can_work(day, time_idx)]

        # Get all the combinations of people who can work on this day
        for people in combinations(people_available, self.min_people_per_slot):
            for person in people:
                person.assign_shift(day, time_idx)

            schedule_copy.assign_shifts(balanced_schedules, idx+1)

            for person in people:
                person.unassign_shift(day, time_idx)

    def __repr__(self) -> str:
        return f'Schedule balance: {self.get_balance()}'
    
    def find_schedules(self, display_fn, top=10):
        balanced_schedules = []
        self.assign_shifts(balanced_schedules, top=top)
        
        # Make dataframe with self.days columns and self.time_slots rows
        df = pd.DataFrame(columns=DAYS_OF_WEEK, index=range(self.time_slots))

        for schedule in balanced_schedules:
            print(schedule)
            for day in range(self.days):
                for time_idx in range(self.time_slots):
                    df[DAYS_OF_WEEK[day]][time_idx] = ', '.join([person.name for person in schedule.people if person.working_days[time_idx][day]])
            display_fn(df)
            print('\n')