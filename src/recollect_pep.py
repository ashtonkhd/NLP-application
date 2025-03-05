"""
Simple script for recollecting PEP-data if needed
"""

import requests
import json
import typing
from bs4 import BeautifulSoup

PEP_METADATA_FILE: str = "./pep_metadata.json"
PEP_DATA_FILE: str = "./pep_data.json"

BAD_STATUS: list[str] = ["Withdrawn", "Superseded"]
GOOD_STATUS: list[str] = ["Active", "Accepted", "Final"]

def getPepContents(pep_data: dict[str, typing.Any]):
    pep_amount: int = len(list(pep_data.keys()))
    new_pep_data = {}
    current: int = 1
    
    for entry in pep_data:
        _current_entry = pep_data[entry]
        _tmp_url = _current_entry["url"]
        _tmp_title = _current_entry["title"]
        _tmp_authors = _current_entry["authors"]
        
        print(f"[{current:03d}/{pep_amount}]", end=" ")
        print(f"GET: {_tmp_url}...", end=" ")
        _response = requests.get(_tmp_url)
        print("Processing...", end=" ")
        _html = BeautifulSoup(_response.content, 'html.parser')
        _paras = _html.find_all('p')
        _paras_content = ""
        _tmp = []
        
        for _para in _paras:
            _tmp.append(_para.get_text())

        _paras_content = " ".join(_tmp)

        new_pep_data.update({entry: {"title": _tmp_title, "authors": _tmp_authors, "url": _tmp_url, "content": _paras_content}})
        print("DONE.")
        
        current += 1

    return new_pep_data

if __name__ == "__main__":
    new_pep_data: dict[str, typing.Any] = {}
    
    with open(PEP_METADATA_FILE, 'r') as target:
        PEP_METADATA = json.load(target)


    for entry in PEP_METADATA.values():
        _number = entry["number"]
        _title = entry["title"]
        _authors = entry["authors"]
        _status = entry["status"]
        _url = entry["url"]

        if _status in GOOD_STATUS:
            new_pep_data.update({f"pep-{_number}": {
                "title": _title,
                "authors": _authors,
                "url": _url}})

    pep_data = getPepContents(new_pep_data)

    with open(PEP_DATA_FILE, 'w', encoding="utf-8") as target:
        json.dump(pep_data, target, ensure_ascii=False, indent=3)
        

