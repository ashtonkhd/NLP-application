from bs4 import BeautifulSoup
import requests

def getHTMLContent(url: str):
    response = requests.get(url)

    return response.text

def main() -> None:
    # The main purpose for the target URL being in a constant here is
    # that it can later be more easily swapped for something else.
    # - Matias S.
    TARGET_URL: str = "https://en.wikipedia.org/wiki/Fish"
    html_content = getHTMLContent(TARGET_URL)

    soup = BeautifulSoup(html_content, 'html.parser')


    # As the task is only to prove that we can get and parse html using
    # beautifulsoup, the program doesn't neccesarily have to do anything
    # complex. So I made it count fish
    fish_count: int = 0
    
    for fish_mention in soup.find_all('p'):
        if "fish" in fish_mention.get_text():
            fish_count += 1

    if fish_count < 100:
        print(f"Chat, this is so sad. The article only mentions Fish {fish_count} times...")

    else:
        print("Wow, we found a lot of fish in that website!")
