

from datetime import datetime, timedelta
from pymongo.cursor import Cursor

class WrongGroupingRangeException(Exception):
    pass

def do_group(collection, start_date_string: str, end_date_string:str, grouping_type:str )->dict:


    try:
        start_date = datetime.strptime(start_date_string, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end_date_string, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise ValueError("Invalid date format")
    group_dates = generate_dates(start_date, end_date, grouping_type)

    match grouping_type:
        case "hour":
            date_string = "%Y-%m-%d T%H"

        case "day":
            date_string = "%Y-%m-%d"

        case "month":
            date_string = "%Y-%m"

        case _:
            raise WrongGroupingRangeException("Invalid grouping type")


    query_results = collection.aggregate([
        {
            "$match": {
                "dt": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": date_string,
                        "date": "$dt"
                    }
                },
                "total": {
                    "$sum": "$value"
                }
            }
        },
        {
            "$sort": {
                "_id":1
            }
        }
    ])

    return query_results_to_output(query_results, group_dates, date_string)
# do_group(collection, "2022-09-01 T00:00:00","2022-12-31 T23:59:00", "month")

def query_results_to_output(query_results:Cursor, group_dates:dict, date_string:str)->dict:

    output = {"dataset": [], "labels": []}
    print(output)

    for result in query_results:
        time = str(datetime.strptime(result["_id"], date_string))

        time = time[:10]+"T"+time[11:]
        if time in group_dates:
            group_dates[time] = result["total"]
        # print(time)

    for date in group_dates:
        output["dataset"].append(group_dates[date])
        output["labels"].append(date)
    return output

def generate_dates(start_date:datetime, end_date:datetime, interval:str)->dict:
    dates = {}
    current_date = start_date

    while current_date <= end_date:

        time = str(current_date)
        time = time[:10]+"T"+time[11:]
        dates[time] = 0
        if interval == 'hour':
            current_date += timedelta(hours=1)
        elif interval == 'day':
            current_date += timedelta(days=1)
        elif interval == 'month':
            # To handle different month lengths, you may need a custom function
            # to add months
            current_date = add_one_month(current_date)

    return dates

# Custom function to add one month to a date
def add_one_month(date:datetime)->datetime:
    next_month = date.replace(day=1)
    if date.month == 12:
        next_month = next_month.replace(year=date.year + 1, month=1)
    else:
        next_month = next_month.replace(month=date.month + 1)
    return next_month

# Define your start and end dates
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 3, 1)

# Generate dates with different intervals
hourly_dates = generate_dates(start_date, end_date, 'hour')
daily_dates = generate_dates(start_date, end_date, 'day')
monthly_dates = generate_dates(start_date, end_date, 'month')





