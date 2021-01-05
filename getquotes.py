import json
import re

import requests
from bs4 import BeautifulSoup

iroh_dialog_regex = re.compile(r"\s*<b>\n\s*Iroh[\s\S]*?<br/>")


def main():
    #iroh_quotes = get_lines_from_episode(iroh_dialog_regex, 1, 1)
    iroh_quotes = []
    for i in range(1, 4):  # 3 seasons
        for j in range(1, 23):  # max 22 episodes per season
            #break
            lines = get_lines_from_episode(iroh_dialog_regex, i, j)
            iroh_quotes += lines
            print("%s quotes scraped from season %d, episode %s\n" % (str(len(lines)).zfill(2), i, str(j).zfill(2)))

    """
    print("Quotes scraped:")
    for quote in iroh_quotes:
        print(quote)
    """
    with open('charlines.json', 'w') as outfile:
        json.dump(convert_to_json(iroh_quotes), outfile, indent=4)


def get_lines_from_episode(character_regex, season, episode):
    lines = []
    webpage = 'http://atla.avatarspirit.net/transcripts.php?num=%d%s' % (season, str(episode).zfill(2))
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, 'html.parser')

    script = soup.find(class_="content")
    script_text = script.prettify()
    #print(script_text)
    iroh_dialog = re.findall(character_regex, script_text)

    for line in iroh_dialog:
        quote = cleanup_dialog(line)
        lines.append(quote)
        print(quote)

    return lines


def cleanup_dialog(line):
    #print(line)
    ugly_text = line.split("\n")
    better_text = []
    for i, word in enumerate(ugly_text):
        ugly_text[i] = word.lstrip()

    #print(ugly_text)
    for word in ugly_text:
        if word is '' or word in ["<b>", "</b>", "<br/>", "<i>", "</i>"]:
            continue
        else:
            better_text.append(word)

    # concatenate all the parts of dialog into one block
    better_text[1] = ' '.join(better_text[1:])

    # clean up the strings
    better_text[0] = re.sub(r":", "", better_text[0])
    better_text[1] = re.sub(r" ?\([^)]+\)", "", better_text[1])
    better_text[1] = re.sub(r": *", "", better_text[1])
    better_text[1] = re.sub(r"^ ", "", better_text[1])

    better_text = tuple(better_text[:2])

    return better_text


def convert_to_json(tuples):
    data = {'lines': []}
    for tup in tuples:
        data['lines'].append({
            'name': tup[0],
            'quote': tup[1],
            'data': None,
            'data_source': None,
        })
    return data


main()
