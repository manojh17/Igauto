import datetime

def today_schedule():

    day = datetime.datetime.now().strftime("%A")

    schedules = {
        "Monday": ["13:00", "13:45", "16:00", "16:45"],
        "Tuesday": ["11:30", "14:00", "16:00", "17:30"],
        "Wednesday": ["12:00", "15:00", "18:00", "20:00"],
        "Thursday": ["11:30", "14:00", "16:00", "17:30"],
        "Friday": ["10:30", "12:30", "15:00", "16:45"],
        "Saturday": ["10:30", "12:30", "15:00", "17:30"],
        "Sunday": ["14:30", "16:00", "17:00", "19:00"],
    }

    return schedules.get(day, [])
