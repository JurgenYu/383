#!/usr/bin/python
import sys
import csv
import datetime

  
# COMPSCI 383 Homework 0 
#  
# Fill in the bodies of the missing functions as specified by the comments and docstrings.


# Exercise 0. (8 points)
#  
def read_data(file_name):
    """Read in the csv file and return a list of tuples representing the data.

    Transform each field as follows:
      date: class date (see datetime module)
      mileage: integer
      location: string
      gallons: float
      price: float

    Do not return a tuple for the header row.  While you can process the rawtext using string
    functions, to receive full credit you must use Python's built in csv module.
    """
    rows = []
    with open(file_name) as csvfile:
        fp = csv.reader(csvfile)
        for row in fp:
            if fp.line_num == 1:
                continue
            if hasMissing(row):
                continue
            else:
                rows.append(tuple([getDate(row[0]), getMilage(row[1]), row[2], getGallons(row[3]), getPrice(row[4])]))
    return rows

# Helper methods
#

def hasMissing(row: list):
    for item in row:
        if item == '':
            return True
    return False

def getDate(date: str):
    dateList = date.split("/")
    return datetime.date(int(dateList[2]), int(dateList[0]), int(dateList[1]))

def getMilage(miles: str):
    return int(miles)

def getGallons(gallons: str):
    return float(gallons)

def getPrice(price: str):
    return float(price[1:])

# Exercise 1. (5 points)
#
def total_cost(rows):
    """Return the total amount of money spent on gas as a float.  Depressing."""
    total = 0.0
    for row in rows:
        total += row[-1] * row[-2]
    return total


# Exercise 2. (5 points)
#
def num_single_locs(rows):
    """Return the number of refueling locations that were visited exactly once."""
    locs = []
    checked = []
    conuts = 0
    for row in rows:
        if row[2] in locs:
            if row[2] in checked:
                continue
            else:
                checked.append(row[2])
                conuts-=1
        else:
            locs.append(row[2])
            conuts+=1
    return conuts


# Exercise 3. (8 points)
#
def most_common_locs(rows):
    """Return a list of the 10 most common refueling locations, along with the number of times
    they appear in the data, in descending order.  Each list item should be a two-element tuple
    of the form (name, count):
    ("Honolulu, HI", 42)

    Hint: store the locations and counts in a dictionary, then convert the dictionary into a list of
    tuples that can be sorted using Python's sorted() or sort() functions (the "Key Functions"
    section of https://docs.python.org/3.6/howto/sorting.html might be helpful).
    """
    locs_list = []
    found = False
    for row in rows:
        for loc in locs_list:
            if loc[0] == row[2]:
                loc[1]+=1
                found = True
                break
        if not found:
            locs_list.append([row[2], 0])
        found = False
    locs_list.sort(key = lambda row:row[1], reverse=True)
    return locs_list[:9]

# Exercise 4. (8 points)
#
def state_totals(rows):
    """Return a dictionary containing the total number of visits (value) for each state as designated by
    the two-letter abbreviation at the end of the location string (keys).  To do this, you'll have to pull
    apart the location string and extract the state abbreviation.

    The return value should be of the form:
        { "CA" -> 42,
          "HI" -> 19,
          etc. }
    """
    state_dict = {}
    for row in rows:
        thisState = row[2][-2:]
        if thisState in state_dict:
            state_dict[thisState]+=1
        else:
            state_dict[thisState]=1
    return state_dict


# Exercise 5. (8 points)
#
def num_unique_dates(rows):
    """Return the total number unique dates in the calendar year that refueling took place.
    (This number should be less than 366!)
    """
    date_list = []
    counts = 0
    for row in rows:
        if [row[0].day, row[0].month] in date_list:
            continue
        else:
            date_list.append([row[0].day, row[0].month])
            counts+=1
    return counts


# Exercise 6. (8 points)
#
def month_avg_price(rows):
    """Return a dictionary containing the average price per gallon as a float (values) for each month (keys).

    Use the functions in Python's datetime module to parse and manipulate the date objects.

    The return value should be of the form:
        { "January" -> 3.12,
          "February" -> 2.89,
          ... }
    """
    month_avg_dict = {}
    dayCountsdict = {}
    for row in rows:
        month = row[0].strftime("%B")
        if month in dayCountsdict:
            dayCountsdict[month]+=1
            month_avg_dict[month]+=row[-1]
        else:
            dayCountsdict[month] = 1
            month_avg_dict[month]+=row[-1]
    for each in month_avg_dict:
        month_avg_dict[each]/=dayCountsdict[each]
    return month_avg_dict  # fix this!


# EXTRA CREDIT (+10 points)
#
def highest_thirty(rows):
    """Return the start and end dates for top three thirty-day periods with the most miles driven.

     The periods should not overlap (you should select them in a greedy manner; that is, find the
     highest mileage period first, and then select the next highest that is outside that window).
     Return a list with the start and end dates (as a Python datetime object) for each period,
     followed by the total mileage, stored in a tuple.  Again, you should use the date wrangling
     functions found in Python's datetime module to manipulate the dates.

    The return value should be of the form:
        [ (1995-02-14, 1995-03-16, 502),
          (1991-12-21, 1992-01-16, 456),
          (1997-06-01, 1997-06-28, 384) ]
    """
    #
    # fill in function body here
    #
    return []  # fix this!


# The main() function below will be executed when your program is run.
# Note that Python does not require a main() function, but it is
# considered good style (as is including the __name__ == '__main__'
# conditional below)
#
def main(file_name):
    rows = read_data(file_name)
    print("Exercise 0: {} rows\n".format(len(rows)))

    cost = total_cost(rows)
    print("Exercise 1: ${:.2f}\n".format(cost))

    singles = num_single_locs(rows)
    print("Exercise 2: {}\n".format(singles))

    print("Exercise 3:")
    for loc, count in most_common_locs(rows):
        print("\t{}\t{}".format(loc, count))
    print("")

    print("Exercise 4:")
    for state, count in sorted(state_totals(rows).items()):
        print("\t{}\t{}".format(state, count))
    print("")

    unique_count = num_unique_dates(rows)
    print("Exercise 5: {}\n".format(unique_count))

    print("Exercise 6:")
    for month, price in sorted(month_avg_price(rows).items(),
                               key=lambda t: datetime.datetime.strptime(t[0], '%B').month):
        print("\t{}\t${:.2f}".format(month, price))
    print("")

    print("Extra Credit:")
    for start, end, miles in sorted(highest_thirty(rows)):
        print("\t{}\t{}\t{} miles".format(start.strftime("%Y-%m-%d"),
                                          end.strftime("%Y-%m-%d"), miles))
    print("")


#########################

if __name__ == '__main__':
    
    data_file_name = sys.argv[1]  # you must pass in the path to the data file
    main(data_file_name)




