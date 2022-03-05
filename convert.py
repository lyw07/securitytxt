import argparse
import json


def convert_csv_to_list(args):
    websites = []
    with open(args.csvfile, "rb") as f:
        for line in f:
            domain = str(line).split(",")[1].rstrip().replace("\\r\\n'", "")
            websites.append(domain)

    with open("top100k.txt", "w") as file:
        json.dump(websites, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process security.txt file on Tranco's most visited websites"
    )
    parser.add_argument("--csvfile", required=True)
    args = parser.parse_args()

    convert_csv_to_list(args)
