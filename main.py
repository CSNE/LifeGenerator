import random
from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta


class NoMoreScheduleException(Exception):
    pass

def randomize(mean, sdev):
    r = random.gauss(mean, sdev)

    minval = mean - sdev * 3
    maxval = mean + sdev * 3

    if r < minval:
        r = minval
    if r > maxval:
        r = maxval

    return r


class DataPoint():
    values_raw = "start_time,end_time,activity,place,address,location,person,food,amount_of_food,meal_type,hunger,emotion,tiredness,temperature,humidity"

    def __init__(self):
        self.values = self.values_raw.split(",")

        for i in self.values:
            setattr(self, i, None)

    def as_csv_row(self):
        vals = []
        for i in self.values:
            vals.append(str(getattr(self, i)))
        return ",".join(vals)

    def validate(self):
        return True


datapoints = []


def add_datapoint(dp):
    assert dp.validate()
    datapoints.append(dp)


def datapoints_to_csv():
    s=''
    s+="start_time,end_time,activity,place,address,location,person,food,amount_of_food,meal_type,hunger,emotion,tiredness,temperature,humidity"
    s+="\n"
    for i in datapoints:
        s+=i.as_csv_row()
        s+="\n"
    return s


def add_move(*,
             environment,
             time_range,
             transportation):
    print("ADD ROW: move")

    dp = DataPoint()
    dp.start_time = time_range[0]
    dp.end_time = time_range[1]
    dp.activity = "이동"
    dp.place = transportation
    dp.location = "실외"
    dp.food = "/"
    dp.amount_of_food = "/"
    dp.meal_type = "/"

    environment.copy_to_datapoint(dp)

    add_datapoint(dp)




def add_eat(*,
            environment,
            time_range,
            food_name,
            food_amount,
            food_type):
    print("ADD ROW: eat")

    dp = DataPoint()
    dp.start_time = time_range[0]
    dp.end_time = time_range[1]
    dp.activity = "식사"
    dp.location = "실내"
    dp.food = food_name
    dp.amount_of_food = food_amount
    dp.meal_type = food_type

    environment.copy_to_datapoint(dp)

    add_datapoint(dp)


def add_work(*,
             environment,
             time_range):
    print("ADD ROW: work")
    dp = DataPoint()
    dp.start_time = time_range[0]
    dp.end_time = time_range[1]
    dp.activity = "업무"
    dp.location = "실내"
    dp.food = "/"
    dp.amount_of_food = "/"
    dp.meal_type = "/"

    environment.copy_to_datapoint(dp)

    add_datapoint(dp)

def add_nothing(*,
                environment,
                time_range):
    print("ADD ROW: nothing")
    dp = DataPoint()
    dp.start_time = time_range[0]
    dp.end_time = time_range[1]
    dp.activity = "아무것도안함"
    dp.location = "실내"
    dp.food = "/"
    dp.amount_of_food = "/"
    dp.meal_type = "/"

    environment.copy_to_datapoint(dp)

    add_datapoint(dp)

class Environment():
    '''
    Stores the current environment, such as time, hunger, and temperature
    '''
    _time = DateTime(2018, 9, 1)
    _hunger = 0
    _emotion = 50
    _tiredness = 0
    _temperature = 25
    _humidity = 50
    _address = "??"
    _place = "??"
    _group = "혼자"

    def __init__(self,*,start_time):
        self._time=start_time


    @property
    def time(self):
        return self._time

    def force_progress_time(self,timedelta):
        self._time+=timedelta

    @property
    def place(self):
        return self._place

    @property
    def address(self):
        return self._address



    def formatted_time(self):
        return self._time.strftime("%H:%M:%S")



    def formatted_hunger(self):
        if self._hunger >= 50:
            return "예"
        elif self._hunger >= 0:
            return "아니오"
        else:
            raise Exception("????")

    def formatted_tiredness(self):
        if self._tiredness >= 80:
            return "매우 높음"
        elif self._tiredness >= 50:
            return "높음"
        elif self._tiredness >= 20:
            return "낮음"
        elif self._tiredness >= 0:
            return "매우 낮음"
        else:
            raise Exception("????")

    def formatted_emotion(self):
        if self._emotion >= 80:
            return "매우 긍정"
        elif self._emotion >= 60:
            return "긍정"
        elif self._emotion >= 40:
            return "보통"
        elif self._emotion >= 20:
            return "부정"
        elif self._emotion >= 0:
            return "매우 부정"
        else:
            raise Exception("????")

    def formatted_temperature(self):
        return self._temperature

    def formatted_humidity(self):
        if self._humidity >= 80:
            return "매우 높음"
        elif self._humidity >= 60:
            return "높음"
        elif self._humidity >= 40:
            return "보통"
        elif self._humidity >= 20:
            return "낮음"
        elif self._humidity >= 0:
            return "매우 낮음"
        else:
            raise Exception("????")

    def formatted_address(self):
        return self._address

    def formatted_place(self):
        return self._place

    def formatted_group(self):
        return self._group

    def copy_to_datapoint(self, dp):

        dp.hunger = self.formatted_hunger()
        dp.emotion = self.formatted_emotion()
        dp.tiredness = self.formatted_tiredness()
        dp.temperature = self.formatted_temperature()
        dp.humidity = self.formatted_humidity()
        dp.address = self.formatted_address()
        dp.person = self.formatted_group()
        dp.place = self.formatted_place()

    def time_progress(self, minutes):
        start_time = self.formatted_time()
        self._time += TimeDelta(minutes=minutes)
        end_time = self.formatted_time()

        self._hunger += minutes/60*10 #10/hour
        self._tiredness += minutes/60*5 #5/hour

        return (start_time, end_time)

    def eat_effect(self):
        self._hunger = 0
        self._emotion += 10

    def sleep_effect(self):
        self._tiredness = 0
        self._emotion += 10

    def move_effect(self, address, place):
        self._address = address
        self._place = place

    def stress_effect(self, factor):
        self._emotion-=factor
        self._tiredness+=factor

    def rest_effect(self,factor):
        self.stress_effect(-factor)


class Human():
    '''
    A single person capable of doing human stuff.
    '''

    def __init__(self,*,
                 start_time):
        self.env = Environment(start_time=start_time)
        self.schedule = ScheduleList()

    def add_schedule(self, schedule):
        self.schedule.add_schedule(schedule)

    def move(self,*,
             minutes_taken,
             transportation,
             dest_address,
             dest_place):

        add_move(environment=self.env,
                 time_range=self.env.time_progress(minutes_taken),
                 transportation=transportation)

        self.env.move_effect(dest_address, dest_place)

    def eat(self,*,
            minutes_taken,
            food_name,
            food_amount,
            food_type):

        add_eat(environment=self.env,
                time_range=self.env.time_progress(minutes_taken),
                food_name=food_name,
                food_amount=food_amount,
                food_type=food_type)

        self.env.eat_effect()

    def work(self,*,minutes_taken):

        add_work(environment=self.env,
                 time_range=self.env.time_progress(minutes_taken))

        self.env.stress_effect(10)

    def do_nothing(self,*,
                   minutes_taken):
        add_nothing(environment=self.env,
                 time_range=self.env.time_progress(minutes_taken))


    def select_action(self):

        print("Selecting action...")
        print("Current time:",self.env.time)

        if not self.schedule.has_schedule():
            raise NoMoreScheduleException

        # Check if need to move
        nearest_event = self.schedule.peek_nearest()

        if ((self.env.address != nearest_event.address) or
                (self.env.place != nearest_event.place)):
            print("Adding move event.")
            self.schedule.add_schedule(
                MoveSchedule(current_environment=self.env,
                             target_schedule=nearest_event)
            )

        # Schedule
        nearest_event = self.schedule.peek_nearest()
        td = nearest_event.start_time - self.env.time

        print("Nearest event:",nearest_event,"\nTime Delta:",td)

        if td < TimeDelta(minutes=0):  # Negative time. start anyway.
            print("SELECTED SCHEDULE(Neg.time):",nearest_event)
            nearest_event.act(self)
            self.schedule.pop_nearest()

        elif td <= TimeDelta(minutes=3):  # ~3minutes remain. discard time and start
            print("SELECTED SCHEDULE:", nearest_event)
            self.env.force_progress_time(td)

            nearest_event.act(self)
            self.schedule.pop_nearest()

        else: #TODO: Placeholder
            print("Add nothing...")
            self.add_schedule(NothingSchedule(start_time=self.env.time,
                                              place=self.env.place,
                                              address=self.env.address,
                                              minutes_duration=td.total_seconds()/60))
    def simulate_until(self, limit_time):

        n=0
        while True:
            n+=1

            print("\n\nCycle",n)

            if n>100:
                print("Over 100 simulation cycles! Breaking.")
                print("Modify source if this is the expected behavior.")
                break
            if limit_time-self.env.time<TimeDelta(0):
                break

            try:
                self.select_action()
            except NoMoreScheduleException:
                print("No more schedule!")
                break



class ScheduleElement():

    def __init__(self,*,
                 start_time,
                 place,
                 address,
                 priority,
                 recurring):
        self.start_time = start_time
        self.place = place
        self.address = address
        self.priority = priority
        self.recurring = recurring

        print("Schedule created.",start_time,"|",place,"|",address)

    def act(self, human):
        raise NotImplementedError


class LectureSchedule(ScheduleElement):

    def __init__(self,*,
                 start_time,
                 place,
                 address,
                 minutes_duration):
        super().__init__(priority=20,
                         recurring=True,
                         start_time=start_time,
                         place=place,
                         address=address)
        self.minutes_duration = minutes_duration

    def act(self, human):
        print("LectureSchedule activated")
        human.work(minutes_taken=self.minutes_duration)


class MeetingSchedule(ScheduleElement):

    def __init__(self,*,
                 start_time,
                 place,
                 address):
        super().__init__(priority=50,
                         recurring=False,
                         start_time=start_time,
                         place=place,
                         address=address)

    def act(self, human):
        raise Exception

class NothingSchedule(ScheduleElement):

    def __init__(self,*,
                 start_time,
                 place,
                 address,
                 minutes_duration):
        super().__init__(priority=50,
                         recurring=False,
                         start_time=start_time,
                         place=place,
                         address=address)
        self.minutes_duration=minutes_duration


    def act(self, human):
        print("NothingSchedule activated")
        human.do_nothing(minutes_taken=self.minutes_duration)

class MoveSchedule(ScheduleElement):
    def __init__(self,*,
                 current_environment,
                 target_schedule):

        self.from_position = (current_environment.address,
                              current_environment.place)
        self.to_position = (target_schedule.address,
                            target_schedule.place)

        self.timetaken = 0
        if current_environment.place != target_schedule.place:
            self.timetaken = 10
        if current_environment.address != target_schedule.address:
            self.timetaken = 30

        super().__init__(priority=0,
                         recurring=False,
                         start_time=target_schedule.start_time - TimeDelta(minutes=self.timetaken),
                         place=current_environment.place,
                         address=current_environment.address)

    def act(self, human):
        print("MoveSchedule activated")
        human.move(minutes_taken=self.timetaken,
                   transportation="PLACEHOLDER",
                   dest_address=self.to_position[0],
                   dest_place=self.to_position[1])


class ScheduleList():
    def __init__(self):
        self._schedule = []

    def add_schedule(self, se):
        self._schedule.append(se)
        self.sort()

    def sort(self):
        self._schedule.sort(key=lambda x: x.start_time)

    def has_schedule(self):
        return len(self._schedule)>0

    def peek_nearest(self):
        return self._schedule[0]


    def pop_nearest(self):
        res = self._schedule[0]
        del self._schedule[0]
        return res


def main():
    h = Human(start_time=DateTime(2018,9,1,9,0,0))
    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018,9,1,12,0,0),
                        place="PLACEHOLDER",
                        address="PLACEHOLDER",
                        minutes_duration=50))

    h.simulate_until(DateTime(2018,9,1,20,0,0))

    print("\n\n\n########  RESULTS  #########\n")
    res=datapoints_to_csv()
    print(res)

    with open("generator_results.csv","w",encoding="utf8") as f:

        f.write(res)




if __name__ == "__main__":
    main()
