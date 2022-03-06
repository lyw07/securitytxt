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
    query_deployment_levels(args)
    query_url_path(args)
    query_protocol(args)
