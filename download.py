import argparse
import random
import threading
import json
import requests

HTTP = "http"
HTTPS = "https"
ROOT = "/"
WELLKNOWN = "/.well-known/"
DEFAULT_HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36"
}
TIMEOUT = 5


def get_website_list(args):
    with open("top100k.txt", "r") as f:
        content = json.load(f)

    websites = content[args.start - 1 : args.end]
    return websites


def run(websites):
    # randomize website list
    random.shuffle(websites)

    for website in websites:
        # send four requests for domain
        threading.Thread(target=crawl, args=(website, HTTP, ROOT)).start()
        threading.Thread(target=crawl, args=(website, HTTPS, ROOT)).start()
        threading.Thread(target=crawl, args=(website, HTTP, WELLKNOWN)).start()
        threading.Thread(target=crawl, args=(website, HTTPS, WELLKNOWN)).start()


def crawl(website, protocol, path):
    url = "{protocol}://{website}{path}security.txt".format(
        protocol=protocol, website=website, path=path
    )

    try:
        resp = requests.get(url, headers=DEFAULT_HEADER, timeout=TIMEOUT)
        if resp.status_code == 200 and (
            resp.headers.get("content-type") is not None
            and "text/plain" in resp.headers.get("content-type")
        ):
            if path == WELLKNOWN:
                filename = "wellknown"
            else:
                filename = "root"

            # create a file with response per request
            with open(
                "results/{}-{}-{}.txt".format(protocol, website, filename), "w"
            ) as file:
                file.write(resp.text)
    except (
        requests.Timeout,
        requests.ConnectionError,
        requests.TooManyRedirects,
    ) as err:
        return
    except Exception as e:
        print("{}: {}\n".format(url, e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download security.txt file on Tranco's most visited websites"
    )
    parser.add_argument("--start", type=int, required=True, help="1, 101, ...")
    parser.add_argument("--end", type=int, required=True, help="100, 1000, ...")
    args = parser.parse_args()

    websites = get_website_list(args)
    run(websites)
