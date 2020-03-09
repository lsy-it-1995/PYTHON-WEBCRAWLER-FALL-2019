import re
from urllib.parse import urlparse
import extract as ex
import tokenizer
import pages

import timer_debug as td

#16091663,75952015

#SEEDURL = https://www.ics.uci.edu,https://www.cs.uci.edu,https://www.informatics.uci.edu,https://www.stat.uci.edu

my_pages = pages.Pages()

timer = td.TimerDebug()


def print_data():
    f = open("HW2output.txt", "w+")
    unique_pages = my_pages.get_all_links_visited()

    # Question 1: How many unique pages did you find? Uniqueness is established by the URL, but discarding the fragment
    # part. So, for example, http://www.ics.uci.edu#aaa and http://www.ics.uci.edu#bbb are the same URL.
    # print("Number Of Unique Pages:",len(unique_pages))
    f.write("Number Of Unique Pages: {0}\n".format(len(unique_pages)))

    # f.write(str("Number Of Unique Pages:", len(unique_pages)))
    largest_page, number_of_tokens = my_pages.get_largest_page()

    # Question 2: What is the longest page in terms of number of words? (HTML markup doesn’t count as words)
    # print("Longest Page:", largest_page, '\t Number Of Words:', number_of_tokens)
    f.write("\nLongest Page: {0} \t Number Of Words: {1}\n".format(largest_page, number_of_tokens))

    # Question 3: What are the 50 most common words in the entire set of pages? (Ignore English stop words, which can
    # be found, for example, here (Links to an external site.)) Submit the list of common words ordered by frequency.
    # print("Fifty Most Common Words")

    all_tokens = my_pages.get_all_tokens()
    all_tokens_freq = tokenizer.compute_word_frequencies(all_tokens)

    fifty_most_common = tokenizer.get_50_most_common_words(all_tokens_freq)

    f.write("\nFifty Most Common Word, freq\n")
    for word, number in fifty_most_common:
        f.write("{0}, {1}\n".format(word, number))
    # print(tokenizer.get_50_most_common_words(all_tokens_freq))

    # Question 4: How many subdomains did you find in the ics.uci.edu domain? Submit the list of subdomains ordered
    # alphabetically and the number of unique su detected in each subdomain. The content of this list should be lines
    # containing URL, number, for example: http://vision.ics.uci.edu, 10 (not the actual number here)
    # print(tokenizer.)
    # print(tokenizer.sort_alpha(my_pages.get_ics_sub_domains()))
    f.write("\nSubdomain(URL), freq(number)\n")
    alpha = tokenizer.sort_alpha(my_pages.get_ics_sub_domains())
    for url, number in alpha:
        f.write("{0}, {1}\n".format(url, number))


def similarity_check(document):
    curr_text = ex.html_to_text(document)
    curr_tokens = tokenizer.tokenize(curr_text)
    curr_freq = tokenizer.compute_word_frequencies(curr_tokens)

    curr_freq = tokenizer.remove_stop_words(curr_freq)

    intersections = tokenizer.find_intersections(curr_freq, my_pages.get_last_tokens_freq())

    numerator = intersections
    denominator = max(max(len(my_pages.get_last_tokens_freq()), len(curr_freq)), 1)
    similarity = numerator / denominator

    print(numerator, '/', denominator, '=', similarity)

    my_pages.set_last_tokens_freq(curr_freq)
    return similarity, curr_tokens


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    timer.set_current_time()
    # print(timer.diff())
    # if timer.diff() > 5:
    #     print(timer.diff())
    #     print('long dl')

    if resp.status != 200 and resp.status != 302:
        # timer.set_last_time()
        return list()

    # get raw html of webpage
    document = resp.raw_response.content

    try:
        if not document[0:150].decode('utf-8').lower().__contains__('<!') and \
                not document[0:150].decode('utf-8').lower().__contains__('html'):
            # print('not html', document[0:50].decode('utf-8'))
            timer.wtf(url+'\n')
            return list()
    except Exception:
        # print('couldn\'t decode:', url)
        timer.wtf('fail:'+url+'\n')
        return list()

    similarity, current_tokens = similarity_check(resp.raw_response.content)
    if similarity >= 0.9:
        return list()

    my_pages.get_all_links_visited()[url] = 1

    subdomain = ex.get_subdomain(url)
    if subdomain in my_pages.get_ics_sub_domains():
        my_pages.get_ics_sub_domains()[subdomain] += 1
    else:
        my_pages.get_ics_sub_domains()[subdomain] = 1

    for current_token in current_tokens:
        my_pages.get_all_tokens().append(current_token)

    my_pages.set_largest_page(url, len(current_tokens))

    # find all links(valid and invalid) on webpage and normalize them
    links = ex.get_link(document, url)

    # links that we will add to the frontier
    valid_links = []

    # look for unique links that are valid, return 200-OK, and are within the specified sub-domains
    for link in links:
        # make sure link is a web url(not a doc, zip, etc...)
        # print(link)
        # if is_valid(link) and not ex.part_of_blacklist(link):
        if is_valid(link):

            # check to see if link is unique
            if link not in my_pages.get_all_links():
                my_pages.get_all_links()[link] = 1
                valid_links.append(link)

            elif link in my_pages.get_all_links():
                my_pages.get_all_links()[link] += 1

    timer.set_last_time()
    return valid_links


def is_valid(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https"]):
            return False

        is_valid_domain = re.match(r".*\.(ics.uci.edu/*)|"
                                   r".*\.(cs.uci.edu/*)|"
                                   r".*\.(informatics.uci.edu/*)|"
                                   r".*\.(stat.uci.edu/*)", ex.get_subdomain(url))

        is_valid_domain = is_valid_domain or re.findall(
            r".(today.uci.edu/department/information_computer_sciences*)", url)



        return is_valid_domain and not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|ppsx|z"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|odc)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise
