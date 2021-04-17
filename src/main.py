# -*- coding: utf-8 -*-

"""
Copy to your clipboard a BibTex generated thanks to the DOI API.
"""

import calendar
import json
import locale
import time

import pyperclip
import requests

locale.setlocale(locale.LC_TIME, "fr_FR")


def logger(level, message):
    """
    Log a message at a specified level

    :param level: The level of printing
    :param message: The message to print

    Example
    -------
    > logger('info', 'hello world')
    [INFO - 17/04/2021 21:37:28] : hello world
    """
    print(f"[{level} - {time.strftime('%d/%m/%Y %H:%M:%S')}] : {message}")


def bibtex_generator(api_result):
    """
    Generate BibTex from the result of DOI API
    and put it in your clipboard.

    :param api_result: The result of DOI API
    """

    # URL
    url = f"howpublished={{\\url{{{api_result['URL']}}} }}"

    # Author
    authors = " and ".join(
        [f"{author['family']}, {author['given']}" for author in api_result["author"]]
    )
    authors = f"author={{{authors}}}"

    # Title
    title = f"title={{{api_result['title']}}}"

    # Year/Month
    temp_date = api_result["created"]["date-parts"][0]
    month = f"month={{{calendar.month_name[temp_date[1]]}}}"
    year = f"year={{{temp_date[0]}}}"

    # ID
    key = f"{api_result['prefix']}_{temp_date[1]}_{temp_date[0]}"

    # Note
    note = (
        f"note={{ [En Ligne] - consulté le {time.strftime('%d')} "
        f"{calendar.month_name[int(time.strftime('%m'))]} {time.strftime('%Y')} }}"
    )

    # Final display
    final = (
        f"@misc{{{key},\n"
        f"{authors},\n"
        f"{title},\n"
        f"{url},\n"
        f"{month},\n"
        f"{year},\n"
        f"{note}}}\n"
    )

    pyperclip.copy(final)

    logger("INFO", "BibTex copy to your clipboard")


print("Enter DOI Number Only URL")

DOI_URL = input()

logger("INFO", "Wait for DOI Lookup")


# GET JSON file
PARAMETER = {"Accept": "application/vnd.citationstyles.csl+json"}

DOI_REQUEST = requests.get(DOI_URL, headers=PARAMETER)
JSON_DOI = DOI_REQUEST.text

if DOI_REQUEST.status_code == 200:
    logger("INFO", f"HTTP Status Code : {DOI_REQUEST.status_code}")
    JSON_LOAD = json.loads(JSON_DOI)
    bibtex_generator(JSON_LOAD)
else:
    logger("ERROR", "Something Wrong")
