# MACS 30122 Final Project
'''
Since the outbreak of Covid-19, the U.S. Congress has introduced and
processed a series of bills responding to the pandemic. Our project aims to
explore the changing patterns of the keywords in the text of legislative bills
introduced in the Congress during 2020, and see if there exists any
correlations between these keyword patterns and the trend in COVID-19 cases in
the U.S. on a monthly basis.
'''

import requests
import bs4
import urllib.parse
import re
import json


def get_soup(url):
    '''
    Takes a webpage's url and returns a BeautifulSoup object.

    Inputs:
        url: URL of a webpage

    Outputs:
        BeautifulSoup object
    '''
    r = requests.get(url)
    page = r.text
    soup = bs4.BeautifulSoup(page, "html5lib")
    return soup


def is_absolute_url(url):
    '''
    Is url an absolute URL?

    Code from PA1 utility.py.
    '''
    if url == "":
        return False
    return urllib.parse.urlparse(url).netloc != ""


def convert_if_relative_url(current_url, new_url):
    '''
    Attempt to determine whether new_url is a relative URL and if so,
    use current_url to determine the path and create a new absolute
    URL.  Will add the protocol, if that is all that is missing.

    Code from PA1 utility.py.

    Inputs:
        current_url: absolute URL
        new_url:

    Outputs:
        new absolute URL or None, if cannot determine that
        new_url is a relative URL.

    Examples:
        convert_if_relative_url("http://cs.uchicago.edu", "pa/pa1.html") yields
            'http://cs.uchicago.edu/pa/pa.html'

        convert_if_relative_url("http://cs.uchicago.edu", "foo.edu/pa.html")
            yields 'http://foo.edu/pa.html'
    '''
    if new_url == "" or not is_absolute_url(current_url):
        return None

    if is_absolute_url(new_url):
        return new_url

    parsed_url = urllib.parse.urlparse(new_url)
    path_parts = parsed_url.path.split("/")

    if len(path_parts) == 0:
        return None

    ext = path_parts[0][-4:]
    if ext in [".edu", ".org", ".com", ".net"]:
        return "http://" + new_url
    elif new_url[:3] == "www":
        return "http://" + new_path
    else:
        return urllib.parse.urljoin(current_url, new_url)


def find_bill_text_urls(soup, url):
    '''
    Finds "a" HTML tags in a BeautifulSoup object and returns a list of
    URLs which direct to the text page (txt format) of bills.

    Inputs:
        soup: BeautifulSoup object
        url: webpage associated with the BeautifulSoup object

    Outputs:
        List of URLs
    '''
    tags = soup.find_all('a')
    tags_abs = []
    for t in tags:
        if t.has_attr('href'):
            abs_url = convert_if_relative_url(url, t['href'])
            if re.match(r'.*bill/\d{1,4}\?', abs_url) is not None:
                url_split = re.split(r'(.*bill/\d{1,4})', abs_url)
                text_url = url_split[1] + "/text?format=txt&" + url_split[2]
                if text_url not in tags_abs:
                    tags_abs.append(text_url)
    return tags_abs


def find_bills(search_page, page_number):
    '''
    Finds all links to bills in a given page.

    Inputs:
        search_page: url of the starting search page
        page_number: search page number

    Outputs:
        List of URLs
    '''
    url = search_page + str(page_number)
    soup = get_soup(url)
    links = find_bill_text_urls(soup, url)
    return links


# Starting search page (with page number removed)
search_covid_bills = "https://www.congress.gov/search?searchResultViewType=\
expanded&q={%22congress%22:[%22116%22,%22117%22],%22source%22:[%22legislation%\
22],%22search%22:%22covid%22,%22type%22:%22bills%22}&pageSize=250&page="

# Scraping all pages
covid_bill_urls = []
for i in range(1, 8):
    covid_bill_urls.extend(find_bills(search_covid_bills, i))


def extract_bill_info(bill_url):
    '''
    Given a url that directs to the text page of a bill, extracts and returns
    the bill's information (full title, bill number, title, introduction date,
    text).

    Inputs:
        bill_url: url of bill's text page

    Outputs:
        Tuple of information on the bill
    '''
    soup = get_soup(bill_url)
    # bill introduction date
    if soup.find("td") is not None:
        sponsor_date = soup.find("td").text
        intro_date = re.search("Introduced (?P<intro_date>\d{2}/\d{2}/\d{4})",
                               sponsor_date).group("intro_date")
    else:
        intro_date = "Not available"
    # bill title info
    if soup.find("title") is not None:
        title_text = soup.find("title").text
        title_text_clean = re.sub(r"\u2013", " ", title_text)
        title_search = re.search("Text - (?P<full_title>.*) \| Congress*",
                                 title_text_clean)
        if title_search is not None:
            full_title = title_search.group("full_title")
            bill_no = re.search("(?P<bill_no>[A-Z].*\d*) - ",
                                full_title).group("bill_no")
            title = re.search("\): (?P<title>.*)", full_title).group("title")
        else:
            full_title = "Not available, see page: " + bill_url
            bill_no = "Not available"
            title = "Not available"
    else:
        full_title = "Not available, see page: " + bill_url
        bill_no = "Not available"
        title = "Not available"
    # bill text
    text_container = soup.find('div', {"id": "billTextContainerTopScrollBar"})
    if text_container is not None:
        text = text_container.next_sibling.text  # raw text
    else:
        text = "Not available, see page: " + bill_url
    return(full_title, bill_no, title, intro_date, text)


def write_bills_json(output_filename, covid_bill_dict):
    '''
    Writes a dictionary of covid bills into a JSON file.

    Inputs:
        output_filename: file name for the JSON file output
        covid_bill_dict: dictionary of covid bills

    Outputs:
        JSON file
    '''
    with open(output_filename, "w") as json_file:
        json.dump(covid_bill_dict, json_file, indent=4)


# Extracting the info for each bill and storing in a dict
# then storing the results in a json file
'''
Sample code: extract first 250 bills (takes approximately 10 minutes to run)
bills_250 = {}
for b_url in covid_bill_urls[0:250]:
    f_title, bill_no, title, intro_date, text = extract_bill_info(b_url)
    bills_250[f_title] = {"intro date" : intro_date,
                          "bill no." : bill_no,
                          "title" : title,
                          "text" : text}
write_bills_json("bills_250.json", bills_250)
'''
# using full dictionary of bills
bills = {}
for b_url in covid_bill_urls:
    f_title, bill_no, title, intro_date, text = extract_bill_info(b_url)
    bills[f_title] = {"intro date": intro_date,
                      "bill no.": bill_no,
                      "title": title,
                      "text": text}
write_bills_json("bills.json", bills)
