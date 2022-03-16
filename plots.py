import matplotlib.pyplot as plt


def plot_deployment_levels():
    old_results = [16, 10, 4, 1]
    new_results = [25, 12.7, 7, 2.2]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    y2 = list(combined[1])
    y3 = list(combined[2])
    y4 = list(combined[3])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".", label="Top 100")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.plot(x, y2, color="darkorange", marker="^", label="Top 1K")
    for i, v in enumerate(y2):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.plot(x, y3, color="g", marker="*", label="Top 10K")
    for i, v in enumerate(y3):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.plot(x, y4, color="r", marker="d", label="Top 100K")
    for i, v in enumerate(y4):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Using security.txt")
    plt.legend()
    plt.show()


def plot_url_path():
    old_results = [65, 18, 17]
    new_results = [58.5, 25.4, 16.1]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    y2 = list(combined[1])
    y3 = list(combined[2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".", label="/.well-known/ Only")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.plot(x, y2, color="darkorange", marker="^", label="Root Only")
    for i, v in enumerate(y2):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.plot(x, y3, color="g", marker="*", label="Both Paths")
    ax.text(0, y3[0] - 2, "%.1f" % y3[0], ha="center")
    ax.text(1, y3[1] + 0.4, "%.1f" % y3[1], ha="center")

    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Aceessing security.txt in URL Path")
    plt.legend()
    plt.show()


def plot_protocol():
    old_results = [6.2, 3.8, 90]
    new_results = [4.0, 0.5, 95.5]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    y2 = list(combined[1])
    y3 = list(combined[2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".", label="Http Only")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.plot(x, y2, color="darkorange", marker="^", label="Https Only")
    for i, v in enumerate(y2):
        ax.text(i, v - 2.5, "%.1f" % v, ha="center")
    plt.plot(x, y3, color="g", marker="*", label="Both Protocols")
    for i, v in enumerate(y3):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")

    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Aceessing security.txt with Protocols")
    plt.legend()
    plt.show()


def plot_expires_use():
    old_results = [1.7]
    new_results = [21]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Having an Expires Field in security.txt")
    plt.ylim([0, 23])
    plt.show()


def plot_encryption_use():
    old_results = [21, 2.5]
    new_results = [39, 14]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    y2 = list(combined[1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".", label="Has an Encryption Field")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.plot(
        x,
        y2,
        color="darkorange",
        marker="^",
        label="Sign the File with an OpenPGP signature",
    )
    for i, v in enumerate(y2):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")

    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Using Encryption and Signatures")
    plt.legend()
    plt.show()


def plot_encryption_values():
    old_results = [91, 4, 0]
    new_results = [97, 2, 0.1]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    y2 = list(combined[1])
    y3 = list(combined[2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".", label="Web URI")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.plot(x, y2, color="darkorange", marker="^", label="OpenPGP Fingerprint")
    for i, v in enumerate(y2):
        ax.text(i, v + 1.0, "%.1f" % v, ha="center")
    plt.plot(x, y3, color="g", marker="*", label="OPENPGPKEY DNS record")
    for i, v in enumerate(y3):
        ax.text(i, v - 1.0, "%.1f" % v, ha="center")

    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Using A Form of Encryption Key")
    plt.legend()
    plt.show()


def plot_preferred_languages_use():
    old_results = [24]
    new_results = [38]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Having a Preferred-Language Field in security.txt")
    plt.ylim([20, 40])
    plt.show()


def plot_policy_use():
    old_results = [50]
    new_results = [44]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Having a Policy Field in security.txt")
    plt.ylim([40, 55])
    plt.show()


def plot_hiring_use():
    old_results = [25]
    new_results = [34]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Having a Hiring Field in security.txt")
    plt.ylim([20, 35])
    plt.show()


def plot_acknowledgments_use():
    old_results = [9]
    new_results = [31]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center")
    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Having a Acknowledgments Field in security.txt")
    plt.show()


def plot_canonical_use():
    old_results = [16]
    new_results = [20]
    x = [0, 1]
    xticks = ["2021-05", "2022-03"]
    combined = list(zip(old_results, new_results))
    y1 = list(combined[0])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y1, color="royalblue", marker=".")
    for i, v in enumerate(y1):
        ax.text(i, v + 0.2, "%.1f" % v, ha="center")
    plt.xticks(x, xticks)
    plt.xlabel("Date")
    plt.ylabel("% of Websites Having a Canonical Field in security.txt")
    plt.ylim([15, 21])
    plt.show()


if __name__ == "__main__":
    plot_deployment_levels()
    plot_url_path()
    plot_protocol()
    plot_expires_use()
    plot_encryption_use()
    plot_encryption_values()
    plot_preferred_languages_use()
    plot_policy_use()
    plot_hiring_use()
    plot_acknowledgments_use()
    plot_canonical_use()
