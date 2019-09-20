import sys

import feupy
import tabulate

COURSES_IDS = {
    "MIEIC"  : 742,
    "LCEEMG" : 738,
    "MIEC"   : 740,
    "MIEIG"  : 725,
    "MIEEC"  : 741,
    "MIEM"   : 743,
    "MIEMM"  : 744,
    "MIEQ"   : 745
}

WEEKDAYS = (
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
)

doc = """A FEUP exams displaying utility.

Usage:
    python exams_table.py <course acronym> [years and ucs_acronyms]

Example:
    python exams_table.py MIEIC 2 ALGE

This will display all the exams of MIEIC's 2nd year curricular units and the Algebra exams.
"""

if len(sys.argv) == 1:
    print(doc)
    exit()

course_acronym = sys.argv[1].upper()

if course_acronym not in COURSES_IDS:
    raise Exception("Unrecognized course acronym")


course = feupy.Course(COURSES_IDS[course_acronym])
exams = course.exams(use_cache = False) # I want the latest version of the page
filtered_exams = []

if len(sys.argv) == 2:
    filtered_exams = exams # This is not a list copy, remember

else: # We need to do some filtering
    options = sys.argv[2:]

    years = []
    ucs_acronyms = []

    for option in options:
        try:
            year = int(option)
            years.append(year)
        except Exception:
            ucs_acronyms.append(option.upper())
    
    for exam in exams:
        uc = exam["curricular unit"]

        if uc.curricular_year in years or uc.acronym in ucs_acronyms:
            filtered_exams.append(exam)

filtered_exams.sort(key = lambda item: item["start"]) # sort chronologically

exams_display = []

for exam in filtered_exams:
    name = exam["curricular unit"].acronym

    day = exam["start"].date()
    weekday = WEEKDAYS[day.weekday()]

    start  = str(exam["start"].time())[:5]
    finish = str(exam["finish"].time())[:5]


    if exam["rooms"] != None:
        rooms = " ".join(exam["rooms"])
    else:
        rooms = None

    exams_display.append(
        [name, day, weekday, start, finish, rooms]
    )

print(tabulate.tabulate(exams_display, headers = ["name", "day", "weekday", "start", "finish", "rooms"]))