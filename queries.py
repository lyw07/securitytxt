import re
import psycopg2
import argparse
import matplotlib.pyplot as plt


def query_deployment_levels(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()
    levels = [100, 1000, 10000, 100000]
    new_results = []
    # query the domains table in the db to get the % of security.txt deployments
    # in different top levels of websites
    for level in levels:
        cur.execute(
            "SELECT COUNT(*) FROM domains WHERE id BETWEEN 1 and {} AND hasfile = true;".format(
                level
            )
        )
        count = cur.fetchone()[0]
        percentage = count / level * 100
        new_results.append(percentage)
        print(
            "{}% of top {} websites have security.txt files deployed.\n".format(
                percentage, level
            )
        )
    cur.close()
    conn.close()

    # draw the images to compare with the original paper's results
    old_results = [16, 10, 4, 1]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    y2 = list(combined[1])
    y3 = list(combined[2])
    y4 = list(combined[3])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".", label="top 100")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.plot(x, y2, color="darkorange", marker="^", label="top 1K")
    for i, v in enumerate(y2):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.plot(x, y3, color="g", marker="*", label="top 10K")
    for i, v in enumerate(y3):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.plot(x, y4, color="r", marker="d", label="top 100K")
    for i, v in enumerate(y4):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Using security.txt")
    plt.legend()
    plt.show()


def query_url_path(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    # only root path
    cur.execute("SELECT COUNT(*) FROM files;")
    total_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM files WHERE root = true AND wellknown = false;")
    root_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have security.txt file only at the root path.\n".format(
            root_percentage
        )
    )
    # only .well-known path
    cur.execute("SELECT COUNT(*) FROM files WHERE root = false AND wellknown = true;")
    wellknown_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have security.txt file only at the .well-known path.\n".format(
            wellknown_percentage
        )
    )
    # both paths
    cur.execute("SELECT COUNT(*) FROM files WHERE root = true AND wellknown = true;")
    both_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have security.txt file at both the root path and the .well-known path.\n".format(
            both_percentage
        )
    )
    cur.close()
    conn.close()


def query_protocol(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    # only http
    cur.execute("SELECT COUNT(*) FROM files;")
    total_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM files WHERE http = true AND https = false;")
    http_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have security.txt files only accessible over HTTP.\n".format(
            http_percentage
        )
    )
    # only https
    cur.execute("SELECT COUNT(*) FROM files WHERE http = false AND https = true;")
    https_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have security.txt files only accessible over HTTPS.\n".format(
            https_percentage
        )
    )
    # both protocols
    cur.execute("SELECT COUNT(*) FROM files WHERE http = true AND https = true;")
    both_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have security.txt files accessible over both protocols.\n".format(
            both_percentage
        )
    )
    cur.close()
    conn.close()


def query_contact_and_openbugbounty_use(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM files;")
    total_count = cur.fetchone()[0]
    # single contact
    cur.execute(
        "SELECT COUNT(*) FROM files WHERE contact != '' AND contact NOT LIKE '%,%';"
    )
    single_contact_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have a single contact field only in the security.txt files.\n".format(
            single_contact_percentage
        )
    )

    # two or more contacts
    cur.execute("SELECT COUNT(*) FROM files WHERE contact LIKE '%,%';")
    two_plus_contact_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have two or more contacts in the security.txt files.\n".format(
            two_plus_contact_percentage
        )
    )

    # no contacts
    cur.execute("SELECT COUNT(*) FROM files WHERE contact = '';")
    no_contact_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have no contacts in the security.txt files.\n".format(
            no_contact_percentage
        )
    )

    # only openbugbounty
    cur.execute(
        "SELECT COUNT(*) FROM files WHERE contact = '' AND openbugbounty != '';"
    )
    openbugbounty_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have openbugbounty field only in the security.txt files.\n".format(
            openbugbounty_percentage
        )
    )

    # both contact and openbugbounty
    cur.execute(
        "SELECT COUNT(*) FROM files WHERE contact != '' AND openbugbounty != '';"
    )
    both_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have both contact and openbugbounty fields in the security.txt files.\n".format(
            both_percentage
        )
    )

    # nothing
    cur.execute("SELECT COUNT(*) FROM files WHERE contact = '' AND openbugbounty = '';")
    nothing_percentage = cur.fetchone()[0] / total_count * 100
    print(
        "{}% of domains have no structured contacts in the security.txt files.\n".format(
            nothing_percentage
        )
    )
    cur.close()
    conn.close()


def query_contact_categories(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT contact FROM files WHERE contact != '';")
    results = cur.fetchall()
    total_count = len(results)

    emails = 0
    urls = 0
    telephones = 0
    others = 0
    both_email_and_url = 0
    for result in results:
        contacts = result[0].split(",")
        email = False
        url = False
        telephone = False
        other = False
        for contact in contacts:
            if "@" in contact:
                email = True
            elif "http" in contact:
                url = True
            elif re.search("[+][1-9]+", contact):
                telephone = True
            else:
                other = True

        if email:
            emails += 1
        if url:
            urls += 1
        if telephone:
            telephones += 1
        if other:
            others += 1
        if email and url:
            both_email_and_url += 1

    print(
        "{}% of domains have emails as contacts.\n".format(emails / total_count * 100)
    )
    print("{}% of domains have urls as contacts.\n".format(urls / total_count * 100))
    print(
        "{}% of domains have both emails and urls as contacts.\n".format(
            both_email_and_url / total_count * 100
        )
    )
    print(
        "{}% of domains have telephone numbers as contacts.\n".format(
            telephones / total_count * 100
        )
    )
    print(
        "{}% of domains have other values as contacts.\n".format(
            others / total_count * 100
        )
    )

    cur.close()
    conn.close()


def query_contact_email_username(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT contact FROM files WHERE contact != '';")
    results = cur.fetchall()

    emails = 0
    usernames = {}
    for result in results:
        contacts = result[0].split(",")
        for contact in contacts:
            if "@" in contact:
                emails += 1
                username = contact.split("@")[0]
                if len(username.split("mailto:")) > 1:
                    username = username.split("mailto:")[1].strip()
                if username in usernames:
                    usernames[username] += 1
                else:
                    usernames[username] = 1

    sorted_usernames = dict(
        sorted(usernames.items(), key=lambda item: item[1], reverse=True)
    )
    for username in sorted_usernames.keys():
        print(
            "{}% of domains that have email contacts have {}@ username.\n".format(
                usernames[username] / emails * 100, username
            )
        )

    cur.close()
    conn.close()


def query_contact_urls(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT contact FROM files WHERE contact != '';")
    results = cur.fetchall()

    count = 0
    hackerone = 0
    openbugbounty = 0
    for result in results:
        contacts = result[0].split(",")
        for contact in contacts:
            if "http" in contact:
                count += 1
                if "hackerone.com" in contact:
                    hackerone += 1
                elif "openbugbounty.org" in contact:
                    openbugbounty += 1

    print(
        "{}% of domains that have urls as contacts list a hackerone.com URL.\n".format(
            hackerone / count * 100
        )
    )

    print(
        "{} domains that have urls as contacts list a openbugbounty.org URL.\n".format(
            openbugbounty
        )
    )

    cur.close()
    conn.close()


def query_expires_use(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM files;")
    total_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE expires != '';")
    expires = cur.fetchone()[0]

    print(
        "{}% of domains that have a Expires field.\n".format(
            expires / total_count * 100
        )
    )

    cur.close()
    conn.close()


def query_expires_values(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM files WHERE expires != '';")
    total_count = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM files WHERE expires LIKE '%2022%' OR expires LIKE '%2023%';"
    )
    good = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE expires LIKE '%2021%';")
    expired = cur.fetchone()[0]

    print(
        "{}% of domains that have a Expires field have valid values.\n".format(
            good / total_count * 100
        )
    )

    print(
        "{}% of domains that have a Expires field have expired values.\n".format(
            expired / total_count * 100
        )
    )

    cur.close()
    conn.close()


def query_encryption_use(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM files;")
    total_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE encryption != '';")
    encryption = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE other LIKE '%signature%';")
    signature = cur.fetchone()[0]

    print(
        "{}% of domains have a Encryption field.\n".format(
            encryption / total_count * 100
        )
    )

    print(
        "{}% of domains have signed the security.txt file.\n".format(
            signature / total_count * 100
        )
    )

    cur.close()
    conn.close()


def query_encryption_values(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM files WHERE encryption != '';")
    encryption = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE encryption LIKE '%https://%';")
    urls = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE encryption LIKE '%openpgp4fpr%';")
    openpgp4fpr = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE encryption LIKE '%dns%';")
    dns = cur.fetchone()[0]

    print(
        "{}% of domains that have a Encryption field use URLs.\n".format(
            urls / encryption * 100
        )
    )

    print(
        "{}% of domains that have a Encryption field use openpgp4fpr URIs.\n".format(
            openpgp4fpr / encryption * 100
        )
    )

    print("{} domains that have a Encryption field use DNS records.\n".format(dns))
    cur.close()
    conn.close()


def query_preferred_languages_use(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM files;")
    total_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE preferredlanguages != '';")
    languages = cur.fetchone()[0]

    print(
        "{}% of domains have a Preferred-Languages field.\n".format(
            languages / total_count * 100
        )
    )

    cur.close()
    conn.close()


def query_preferred_languages_values(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT preferredlanguages FROM files WHERE preferredlanguages != '';")
    results = cur.fetchall()

    values = {}
    for result in results:
        languages = result[0].split(",")
        for language in languages:
            language = language.strip()
            if language in values:
                values[language] += 1
            else:
                values[language] = 1

    sorted_values = dict(sorted(values.items(), key=lambda item: item[1], reverse=True))
    for language in sorted_values.keys():
        print(
            "{}% of domains that have a Preferred-Language field lists {}.\n".format(
                sorted_values[language] / len(results) * 100, language
            )
        )

    cur.close()
    conn.close()


def query_policy_use(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM files;")
    total_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE policy != '';")
    policy = cur.fetchone()[0]

    print("{}% of domains have a Policy field.\n".format(policy / total_count * 100))

    cur.close()
    conn.close()


def query_policy_values(args):
    # create a database connection
    conn = psycopg2.connect(
        host="localhost", database=args.dbname, user=args.dbuser, password=args.dbpass
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM files WHERE policy != '';")
    policy = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE policy LIKE '%https://%';")
    webpages = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE policy LIKE '%hackerone.com%';")
    hackerone = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM files WHERE policy LIKE '%bugcrowd.com%';")
    bugcrowd = cur.fetchone()[0]

    print(
        "{}% of domains that have a Policy field use a webpage.\n".format(
            webpages / policy * 100
        )
    )
    print(
        "{}% of domains that have a Policy field use a hackerone.com page.\n".format(
            hackerone / policy * 100
        )
    )
    print(
        "{}% of domains that have a Policy field use a bugcrowd.com page.\n".format(
            bugcrowd / policy * 100
        )
    )

    cur.close()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Query security.txt file content from the database"
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
    # query_deployment_levels(args)
    # query_url_path(args)
    # query_protocol(args)
    # query_contact_and_openbugbounty_use(args)
    # query_contact_categories(args)
    # query_contact_email_username(args)
    # query_contact_urls(args)
    # query_expires_use(args)
    # query_expires_values(args)
    # query_encryption_use(args)
    # query_encryption_values(args)
    # query_preferred_languages_use(args)
    # query_preferred_languages_values(args)
    # query_policy_use(args)
    query_policy_values(args)
