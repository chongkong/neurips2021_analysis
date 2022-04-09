import sys

import requests
from bs4 import BeautifulSoup

page = requests.get("https://nips.cc/Conferences/2021/AcceptedPapersInitial")
soup = BeautifulSoup(page.text, "html.parser")

pp_ids = []
for link in soup.find_all("div", {"class": "maincard narrower poster"}):
    pp_ids.append(link.get("id").split("_")[1])

pp_names = []
pp_authors = []

for i, pp_id in enumerate(pp_ids, start=1):
    pp_soup = BeautifulSoup(
        requests.get(f"https://nips.cc/Conferences/2021/Schedule?showEvent={pp_id}").text, "html.parser"
    )
    pp_name = pp_soup.find("div", {"class": "maincardBody"}).get_text()
    pp_names.append(pp_name)
    authors = []

    for author in pp_soup.find_all("button", {"class": "btn btn-default"}):
        at_id = author.get("onclick")
        at_id = at_id[at_id.find("('") + 2 : at_id.find("')")]
        at_soup = BeautifulSoup(
            requests.get(f"https://neurips.cc/Conferences/2021/Schedule?showSpeaker={at_id}").text, "html.parser"
        )
        at_name = at_soup.find("h3").get_text()
        ins_name = at_soup.find("h4").get_text()
        authors.append(f"{at_name} ({ins_name})")

    pp_authors.append(authors)
    print(f"Processing {i}/{len(pp_ids)}", file=sys.stderr)

    with open("pp_names.txt", "a") as f:
        print(pp_name, file=f)

    with open("pp_authors.txt", "a") as f:
        print('\n'.join(authors), file=f)
