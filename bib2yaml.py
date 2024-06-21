import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text
import yaml

input_file = "pubs.bib"
output_file = "pubs.yml"

lt = LatexNodes2Text()

months_dict_to_num = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12
}

new_output = []


def null_checker(bib_entry, key):
    return bib_entry[key] if key in bib_entry and bib_entry[key] is not None else None


with open(input_file) as f:
    db = bibtexparser.load(f)


for entry in db.entries:

    # TODO: Check if the any of the visible name is same as the CV author, if yes then encapsulate in "***"

    authors = [author.strip() for author in entry["author"].split("and")]
    if len(authors) > 7:
        authors = [authors[0], "et al."]

    filtered_entry = {
        "title": entry["title"],
        "authors": authors,
        "journal": null_checker(entry, "journal"),
        "doi": null_checker(entry, "doi"),
        "url": null_checker(entry, "url"),
    }

    year = entry.get("year")
    month = entry.get("month").lower() if entry.get("month") else None

    if year:
        full_date = str(year)
        if month:
            full_date = f"{year}-{months_dict_to_num[month]:02d}"

    filtered_entry["date"] = full_date

    new_output.append({key: value for key, value in filtered_entry.items() if value is not None})

with open(output_file, "w") as yaml_file:
    yaml.dump(new_output, yaml_file, sort_keys=False)

print(f"Filtered entries have been written to {output_file}")