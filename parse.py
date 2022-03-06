import json
import psycopg2
import os
import argparse

HTTP = "http"
HTTPS = "https"
ROOT = "root"
WELLKNOWN = "wellknown"


def cleanup_response():
    for f in os.listdir("results"):
        if f == ".DS_Store":
            continue
        fname = os.path.join("results", f)
        if os.path.isfile(fname):
            with open(fname) as file:
                try:
                    c = file.read()
                except UnicodeDecodeError:
                    os.remove(fname)
                    continue
            content = c.lower()
            if (
                "doctype" in content
                or "<html>" in content
                or "not found" in content
                or "couldn't find" in content
                or "</div>" in content
                or "uptodate.com" in fname
            ):
                os.remove(fname)
                continue

            if (
                "contact:" not in content
                and "expires:" not in content
                and "encryption:" not in content
                and "acknowledgments:" not in content
                and "preferred-languages:" not in content
                and "canonical:" not in content
                and "policy:" not in content
                and "hiring:" not in content
                and "openbugbounty:" not in content
                and "hackerone" not in content
                and "security" not in content
                and "vulnerability" not in content
                and "contacter" not in content
            ):
                os.remove(fname)


def init_db(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()
    with open("top100k.txt", "r") as f:
        websites = json.load(f)

    for i in range(len(websites)):
        domain = websites[i]
        hasfile = False
        for protocol in [HTTP, HTTPS]:
            if hasfile:
                break
            for path in [ROOT, WELLKNOWN]:
                filename = "results/{}-{}-{}.txt".format(protocol, domain, path)
                if os.path.exists(filename):
                    cur.execute(
                        "INSERT INTO domains (index, domain, hasfile) VALUES (%s, %s, %s)",
                        (i + 1, domain, True),
                    )
                    hasfile = True
                    break
        if not hasfile:
            cur.execute(
                "INSERT INTO domains (index, domain, hasfile) VALUES (%s, %s, %s)",
                (i + 1, domain, False),
            )
    conn.commit()
    cur.close()
    conn.close()


def write_to_db(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()
    visited = []
    for f in os.listdir("results"):
        if f == ".DS_Store":
            continue
        values = f.split("-", 1)
        protocol = values[0]
        vals = values[1].rsplit("-", 1)
        domain = vals[0]
        path = vals[1].split(".txt")[0]
        filename = os.path.join("results", f)
        # If the domain has been parsed, then only need to update the values of
        # supported protocol and path in the db
        if domain in visited:
            cur.execute(
                "UPDATE files SET {} = true, {} = true WHERE domain = '{}'".format(
                    protocol, path, domain
                ),
            )
            continue
        visited.append(domain)

        fields = {
            "contact": "",
            "openbugbounty": "",
            "expires": "",
            "encryption": "",
            "preferredlanguages": "",
            "policy": "",
            "hiring": "",
            "acknowledgments": "",
            "canonical": "",
        }
        other = ""
        with open(filename, "r") as file:
            for line in file.readlines():
                content = line.lower()
                # comment line, skip
                if content.startswith("#") or content.strip() == "":
                    continue

                match_field = False
                for field in fields.keys():
                    if field == "preferredlanguages":
                        field_name = "preferred-languages"
                    else:
                        field_name = field
                    # line matches field patterns
                    if content.startswith("{}:".format(field_name)):
                        c = content.split("{}:".format(field_name))[1].strip()
                        if fields[field] != "":
                            fields[field] = fields[field] + "," + c
                        else:
                            fields[field] += c
                        match_field = True
                        break
                # if the line does not match with any field patterns
                if not match_field:
                    if other != "":
                        other = other + "," + content
                    else:
                        other += content

        cur.execute(
            "INSERT INTO files (domain, http, https, root, wellknown, contact, openbugbounty, expires, encryption, preferredlanguages, policy, hiring, acknowledgments, canonical, other) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                domain,
                protocol == "http",
                protocol == "https",
                path == "root",
                path == "wellknown",
                fields["contact"],
                fields["openbugbounty"],
                fields["expires"],
                fields["encryption"],
                fields["preferredlanguages"],
                fields["policy"],
                fields["hiring"],
                fields["acknowledgments"],
                fields["canonical"],
                other,
            ),
        )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse security.txt file on Tranco's most visited websites"
    )
    parser.add_argument(
        "--dbname",
        required=True,
        help="Name of the database to store security.txt content",
    )
    parser.add_argument(
        "--dbuser", required=True, help="Username to the database connection"
    )
    parser.add_argument(
        "--dbpass", required=True, help="Password to the database connection"
    )
    args = parser.parse_args()

    cleanup_response()
    init_db(args)
    write_to_db(args)
