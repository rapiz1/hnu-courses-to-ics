import datetime
import json
import ics
data = json.load(open('data.json', 'r'))['data']
# 在这里修改开学第一周周一的日期
start_date = datetime.date(2020, 2, 17)

c = ics.Calendar()

def adjust_time(time:str):
    time = str(time).rjust(4, '0')
    time = time[:2]+':'+time[2:]+'+08:00'
    return time

def create_lesson(lesson):
    name = lesson['kc_name']
    description = f"{lesson['teachernames']} {lesson['js_name']}"
    weeks = lesson['pkzcmx'].split(',')
    weekday = int(lesson['pksjmx'][0][0])
    weeks = map(lambda x: int(x), weeks)
    try:
        for week in weeks:
            date = start_date + datetime.timedelta(weeks=week-1,days=weekday-1)
            print(name, date, description)
            btime = datetime.time.fromisoformat(adjust_time(lesson['idjkssj']))
            etime = datetime.time.fromisoformat(adjust_time(lesson['idjjssj']))
            
            e = ics.Event(name, datetime.datetime.combine(date, btime), datetime.datetime.combine(date, etime), description=description, location=lesson['js_name'],
                        organizer=lesson['teachernames'], attendees=lesson['ktmc_name'].split(','))
            #e = ics.Event(name, datetime.datetime.combine(date,btime), datetime.datetime.combine(date,etime), description=description)
            c.events.add(e)
    except Exception as err:
        print(name, err)


for lesson in data:
    create_lesson(lesson)
with open('output.ics', 'w') as f:
    f.write(str(c))
