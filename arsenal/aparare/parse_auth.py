import argparse
import re
import sys
from collections import Counter


TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port\b")


def esec(linie):
    rezultat = TIPAR.search(linie)
    if rezultat is None:
        return None
    return rezultat.group(1), rezultat.group(2)


def citeste_esecuri(cale):
    esecuri = []
    try:
        with open(cale, encoding="utf-8", errors="replace") as jurnal:
            for linie in jurnal:
                rezultat = esec(linie)
                if rezultat is not None:
                    user, ip = rezultat
                    esecuri.append({"user": user, "ip": ip})
    except FileNotFoundError:
        print("nu gasesc", cale, file=sys.stderr)
    return esecuri


def pe_ip(esecuri):
    return Counter(esec["ip"] for esec in esecuri)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("log")
    args = parser.parse_args()
    esecuri = citeste_esecuri(args.log)
    counts = pe_ip(esecuri)

    print(f"Esecuri de autentificare: {len(esecuri)}")
    for ip, numar in counts.most_common():
        print(f"  {ip}: {numar}")


if __name__ == "__main__":
    main()
