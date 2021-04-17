import requests
import json
import time
import calendar
import pyperclip
import locale

locale.setlocale(locale.LC_TIME, "fr_FR")


def Logger(level, message):
    print(f"[{level} - {time.strftime('%d/%m/%Y %H:%M:%S')}] : {message}")


def BibTexGenerator(api_result):
    ## URL
    URL = f"howpublished={{\\url{{{api_result['URL']}}} }}"

    ### Author
    AUTHORS = " and ".join(
        [f"{author['family']}, {author['given']}" for author in api_result["author"]]
    )
    AUTHORS = f"author={{{AUTHORS}}}"

    ### Title
    TITLE = f"title={{{api_result['title']}}}"

    ### Year/Month
    temp_date = api_result["created"]
    temp_date = temp_date["date-parts"][0]
    DATE = f"month={{{calendar.month_name[temp_date[1]]}}},\nyear={{{temp_date[0]}}}"

    ## ID
    KEY = f"{api_result['prefix']}_{temp_date[1]}_{temp_date[0]}"

    ## Note
    NOTE = f"note={{ [En Ligne] - consulté le {time.strftime('%d')} {calendar.month_name[int(time.strftime('%m'))]} {time.strftime('%Y')} }}"

    ## Final display
    FINAL = (
        f"@misc{{{KEY},\n"
        f"{AUTHORS},\n"
        f"{TITLE},\n"
        f"{URL},\n"
        f"{DATE},\n"
        f"{NOTE}}}\n"
    )

    pyperclip.copy(FINAL)

    Logger("INFO", "BibTex copy to your clipboard")


print("Enter DOI Number Only URL")

DOI_URL = input()

Logger("INFO", "Wait for DOI Lookup")


## GET JSON file
PARAMETER = {"Accept": "application/vnd.citationstyles.csl+json"}

DOI_REQUEST = requests.get(DOI_URL, headers=PARAMETER)
JSON_DOI = DOI_REQUEST.text

if DOI_REQUEST.status_code == 200:
    Logger("INFO", f"HTTP Status Code : {DOI_REQUEST.status_code}")
    JSON_LOAD = json.loads(JSON_DOI)
    BibTexGenerator(JSON_LOAD)
else:
    Logger("ERROR", "Something Wrong")
