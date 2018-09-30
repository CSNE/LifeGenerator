import random
from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta
import math

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

def add_meet(*,
             environment,
             time_range):
    print("ADD ROW: meet")
    dp = DataPoint()
    dp.start_time = time_range[0]
    dp.end_time = time_range[1]
    dp.activity = "사교"
    dp.location = "실내"
    dp.food = "/"
    dp.amount_of_food = "/"
    dp.meal_type = "/"

    environment.copy_to_datapoint(dp)

    add_datapoint(dp)


def add_sleep(*,
             environment,
             time_range):
    print("ADD ROW: sleep")
    dp = DataPoint()
    dp.start_time = time_range[0]
    dp.end_time = time_range[1]
    dp.activity = "수면"
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

class Parameters():
    home_addr="HOMEADDR"
    home_place="HOMEPLACE"

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

    _temperature_curve=lambda t:25

    def __init__(self,*,start_time):
        self._time=start_time


    def set_tempcurve(self,tc):
        self._temperature_curve=tc

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

    @property
    def hunger(self):
        return self._hunger

    def formatted_time(self):
        return self._time.strftime("%Y-%m-%d %H:%M:%S")


    def group_set(self,group):
        self._group=group
    def group_clear(self):
        self._group="혼자"

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
        return int(self._temperature)

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
        if minutes<0:
            raise ValueError("Negative minutes????",minutes)
        start_time = self.formatted_time()
        self._time += TimeDelta(minutes=minutes)
        end_time = self.formatted_time()

        self._hunger += minutes/60*10 #10/hour
        self._tiredness += minutes/60*5 #5/hour

        self._temperature=self._temperature_curve(self.time.hour+self.time.minute/60)

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
                 start_time,
                 parameters):
        self.env = Environment(start_time=start_time)
        self.schedule = ScheduleList()
        self.parameters=parameters

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

    def sleep(self,*,minutes_taken):

        add_sleep(environment=self.env,
                 time_range=self.env.time_progress(minutes_taken))

        self.env.sleep_effect()

    def meet(self,*,minutes_taken):

        add_meet(environment=self.env,
                 time_range=self.env.time_progress(minutes_taken))

    def do_nothing(self,*,
                   minutes_taken):
        add_nothing(environment=self.env,
                 time_range=self.env.time_progress(minutes_taken))

    def minutes_clearance(self):
        return (self.schedule.peek_nearest().start_time-self.env.time).total_seconds()/60
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

        else: #No schedule. Generate a new one.
            print("Generating a new schedule...")

            eat_probability = self.parameters.eat_probability(self.env.hunger)
            # Snacks
            if eat_probability > random.random() and self.minutes_clearance()>30:
                self.schedule.add_schedule(
                    SnackSchedule(
                        start_time=self.env.time+TimeDelta(minutes=10),
                        place="편의점",
                        address=self.env.address,
                        food_type="PLACEHOLDER",
                        food_name="PLACEHOLDER",
                        food_amount="PLACEHOLDER",
                        minutes_duration=10
                    )
                )
            else:
                self.add_schedule(NothingSchedule(start_time=self.env.time,
                                                  place=self.env.place,
                                                  address=self.env.address,
                                                  minutes_duration=min(3600,td.total_seconds())/60))

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
                 priority):
        self.start_time = start_time
        self.place = place
        self.address = address
        self.priority = priority

        print("Schedule created.",start_time,"|",place,"|",address)

    def act(self, human):
        raise NotImplementedError



    def readd(self):
        return False


class LectureSchedule(ScheduleElement):

    def __init__(self,*,
                 start_time,
                 place,
                 address,
                 minutes_duration,
                 friend=None):
        super().__init__(priority=20,
                         start_time=start_time,
                         place=place,
                         address=address)
        self.minutes_duration = minutes_duration
        self.friend=friend

    def act(self, human):
        print("LectureSchedule activated")

        if self.friend is not None:
            human.env.group_set(self.friend)
        human.work(minutes_taken=self.minutes_duration)
        human.env.group_clear()



    def readd(self):
        self.start_time+=TimeDelta(days=7)
        return True

class SleepSchedule(ScheduleElement):

    def __init__(self,*,
                 start_time,
                 place,
                 address,
                 wake_time,
                 jitter_sdev):
        super().__init__(priority=20,
                         start_time=start_time,
                         place=place,
                         address=address)
        self.wake_time = wake_time
        self.jitter_sdev=jitter_sdev
        self.orig_start_time=start_time

    def act(self, human):
        print("SleepSchedule activated")
        human.sleep(
            minutes_taken=(
                (self.wake_time-human.env.time).total_seconds()/60
            )
        )

    def readd(self):
        self.orig_start_time+=TimeDelta(days=1)
        self.start_time=self.orig_start_time+TimeDelta(minutes=randomize(0,self.jitter_sdev))
        self.wake_time+=TimeDelta(days=1)
        return True



class MeetingSchedule(ScheduleElement):

    def __init__(self,*,
                 start_time,
                 place,
                 address,
                 person,
                 minutes_duration):
        super().__init__(priority=50,
                         start_time=start_time,
                         place=place,
                         address=address)
        self.person=person
        self.minutes_taken=minutes_duration
    def act(self, human):
        human.env.group_set(self.person)
        human.work(minutes_taken=self.minutes_taken)
        human.env.group_clear()

class SnackSchedule(ScheduleElement):

    def __init__(self,*,
                 start_time,
                 place,
                 address,
                 minutes_duration,
                 food_amount,
                 food_name,
                 food_type):

        super().__init__(priority=50,
                         start_time=start_time,
                         place=place,
                         address=address)

        self.minutes_duration=minutes_duration
        self.food_amount =food_amount
        self.food_name =food_name
        self.food_type =food_type

    def act(self, human):
        print("SnackSchedule activated")
        human.eat(minutes_taken=self.minutes_duration,
                  food_amount=self.food_amount,
                  food_name=self.food_name,
                  food_type=self.food_type)

class MealSchedule(ScheduleElement):

    def __init__(self,*,
                 start_time,
                 place,
                 address,
                 minutes_duration,
                 food_amount,
                 food_name,
                 food_type):

        super().__init__(priority=50,
                         start_time=start_time,
                         place=place,
                         address=address)

        self.minutes_duration=minutes_duration
        self.food_amount =food_amount
        self.food_name =food_name
        self.food_type =food_type

    def act(self, human):
        print("MealSchedule activated")
        human.eat(minutes_taken=self.minutes_duration,
                  food_amount=self.food_amount,
                  food_name=self.food_name,
                  food_type=self.food_type)
    def readd(self):
        self.start_time+=TimeDelta(days=7)
        return True

class NothingSchedule(ScheduleElement):

    def __init__(self,*,
                 start_time,
                 place,
                 address,
                 minutes_duration):
        super().__init__(priority=50,
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
        if not res.readd():
            del self._schedule[0]
        self.sort()
        return res


def main():
    p=Parameters()
    p.home_addr = "HOMEADDR"
    p.home_place = "HOMEPLACE"
    p.school_addr="SCHOOLADDR"
    p.school_cafeteria_place="SCHOOLFOODPLACE"
    def eat_probability(hunger):
        if hunger < 50:
            return 0

        return (hunger - 50) / 50 * 0.7 + 0.3
    p.eat_probability=eat_probability
    def temperature_curve(hour):
        return 25+5*math.sin((hour-6)/24*2*math.pi)+randomize(0,3)

    h = Human(start_time=DateTime(2018,9,2,20,0,0),
              parameters=p)

    h.env.set_tempcurve(temperature_curve)

    h.add_schedule(
        SleepSchedule(start_time=DateTime(2018, 9, 2, 23, 0, 0),
                      place=p.home_place,
                      address=p.home_addr,
                      wake_time=DateTime(2018, 9, 3, 7, 0, 0),
                      jitter_sdev=30)
    )


    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018,9,3,11,0,0),
                        place="공A131",
                        address=p.school_addr,
                        minutes_duration=170,
                        friend="친밀한 사람|영희")
    )

    h.add_schedule(
        MealSchedule(start_time=DateTime(2018,9,3,14,0,0),
                     place="학생회관",
                     address=p.school_addr,
                     minutes_duration=30,
                     food_amount="PLACEHOLDER",
                     food_name="PLACEHOLDER",
                     food_type="PLACEHOLDER"
                     )
    )

    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018, 9, 3, 15, 0, 0),
                        place="공D504",
                        address=p.school_addr,
                        minutes_duration=110)
    )


    #TUE

    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018, 9, 4, 9, 0, 0),
                        place="과111",
                        address=p.school_addr,
                        minutes_duration=50,
                        friend="친밀한 사람|영희")
    )
    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018, 9, 4, 10, 0, 0),
                        place="공D509",
                        address=p.school_addr,
                        minutes_duration=50)
    )
    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018, 9, 4, 11, 0, 0),
                        place="대강당",
                        address=p.school_addr,
                        minutes_duration=50)
    )
    h.add_schedule(
        MealSchedule(start_time=DateTime(2018, 9, 4, 12, 0, 0),
                     place="학생회관",
                     address=p.school_addr,
                     minutes_duration=30,
                     food_amount="PLACEHOLDER",
                     food_name="PLACEHOLDER",
                     food_type="PLACEHOLDER"
                     )
    )
    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018, 9, 4, 13, 0, 0),
                        place="위B09",
                        address=p.school_addr,
                        minutes_duration=110,
                        friend="친밀한 사람|철수")
    )


    #WED
    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018, 9, 5, 10, 0, 0),
                        place="공D504",
                        address=p.school_addr,
                        minutes_duration=110)
    )
    h.add_schedule(
        MealSchedule(start_time=DateTime(2018, 9, 5, 12, 0, 0),
                     place="학생회관",
                     address=p.school_addr,
                     minutes_duration=30,
                     food_amount="PLACEHOLDER",
                     food_name="PLACEHOLDER",
                     food_type="PLACEHOLDER"
                     )
    )
    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018, 9, 5, 13, 0, 0),
                        place="공D504",
                        address=p.school_addr,
                        minutes_duration=50)
    )

    # THR
    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018, 9, 6, 10, 0, 0),
                        place="과111",
                        address=p.school_addr,
                        minutes_duration=110)
    )
    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018, 9, 6, 12, 0, 0),
                        place="위B09",
                        address=p.school_addr,
                        minutes_duration=50)
    )
    h.add_schedule(
        MealSchedule(start_time=DateTime(2018, 9, 6, 13, 0, 0),
                     place="학생회관",
                     address=p.school_addr,
                     minutes_duration=30,
                     food_amount="PLACEHOLDER",
                     food_name="PLACEHOLDER",
                     food_type="PLACEHOLDER"
                     )
    )
    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018, 9, 6, 15, 0, 0),
                        place="공D509",
                        address=p.school_addr,
                        minutes_duration=110)
    )

    #FRI
    h.add_schedule(
        LectureSchedule(start_time=DateTime(2018, 9, 7, 11, 0, 0),
                        place="공D504",
                        address=p.school_addr,
                        minutes_duration=50)
    )


    #Extra
    h.add_schedule(
        MeetingSchedule(
            start_time=DateTime(2018,9,7,14,0,0),
            place="신촌역",
            address=p.school_addr,
            person="데면한 관계|홍길동",
            minutes_duration=60
        )
    )

    h.simulate_until(DateTime(2018,9,30,20,0,0))

    print("\n\n\n########  RESULTS  #########\n")
    res=datapoints_to_csv()
    print(res)

    with open("generator_results.csv","w",encoding="utf8") as f:

        f.write(res)

if __name__ == "__main__":
    main()
