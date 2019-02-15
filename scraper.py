import os
import shutil

import requests
from bs4 import BeautifulSoup


def go_to_ch_dir(chapter_dir_name: str):
    if not os.path.isdir(chapter_dir_name):
        os.mkdir(chapter_dir_name)
    os.chdir(chapter_dir_name)


def scrape_worm(start_link: str):
    if start_link is None:
        return
    with requests.get(start_link) as page:
        soup = BeautifulSoup(page.content, "html.parser")
        ch_title = soup.find("h1", class_="entry-title").get_text()
        print(ch_title)

        links = soup.find_all("a")
        next_link = None
        if links != None:
            for link in links:
                if link.get_text().strip().lower() == "next chapter":
                    next_link = link.get("href")

        ch_content = soup.find("div", class_="entry-content")
        ps = ch_content.find_all("p")
        del ps[0], ps[-1]

        with open(f"{ch_title}.html", "w") as ofp:
            ofp.write(
                f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>{ch_title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="main.css">
</head>
<body>
    {"".join([p.prettify() for p in ps])}
</body>
</html>
                """
            )

        scrape_worm(next_link)


def main():
    chapter_dir_name = "chapters"
    ch1_link = r"https://parahumans.wordpress.com/2011/06/11/1-1/"

    go_to_ch_dir(chapter_dir_name)
    scrape_worm(ch1_link)


if __name__ == "__main__":
    main()
