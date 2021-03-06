import os

import requests
from bs4 import BeautifulSoup


def go_to_ch_dir(chapter_dir_name: str):
    if not os.path.isdir(chapter_dir_name):
        os.mkdir(chapter_dir_name)
    os.chdir(chapter_dir_name)


def scrape_worm(cur_link: str, prev_fn=None, ch_no=1):
    prev_fn = None
    while cur_link is not None:
        page = requests.get(cur_link)
        # with requests.get(cur_link) as page:
        soup = BeautifulSoup(page.content, "html.parser")
        ch_title = soup.find("h1", class_="entry-title").get_text()
        cur_fn = f"{ch_no}-{ch_title}.html"
        print(cur_fn)

        links = soup.find_all("a")
        next_link = None
        if links:
            for link in links:
                if link.get_text().strip().lower() == "next chapter":
                    next_link = link.get("href")

        next_fn = None
        if next_link:
            with requests.get(next_link) as next_page:
                next_soup = BeautifulSoup(next_page.content, 'html.parser')
                next_title = next_soup.find(
                    "h1", class_="entry-title").get_text()
                next_fn = f"{ch_no+1}-{next_title}.html" if next_title else None

        ch_content = soup.find("div", class_="entry-content")
        ps = ch_content.find_all("p")
        del ps[0], ps[-1]

        with open(cur_fn, "w") as ofp:
            ofp.write(
                    f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>{ch_title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="../main.css">
</head>
<body>
    <header>
        <h1>{ch_title}</h1>
    </header>
    <main>
        {"".join([p.prettify() for p in ps])}
    </main>
    <footer>
        {f'<a id="prevChapter" href="{prev_fn}">Previous Chapter</a>' if prev_fn else ""}
        {f'<a id="nextChapter" href="{next_fn}">Next Chapter</a>' if next_fn else ""}
    </footer>
</body>
</html>
                """
                )
        page.close()
        prev_fn = cur_fn
        cur_link = next_link
        ch_no += 1


def main():
    chapter_dir_name = "chapters"
    ch1_link = r"https://parahumans.wordpress.com/2011/06/11/1-1/"

    go_to_ch_dir(chapter_dir_name)
    scrape_worm(ch1_link)


if __name__ == "__main__":
    main()
