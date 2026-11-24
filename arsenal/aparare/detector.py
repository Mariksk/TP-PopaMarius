import argparse
import json

from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip


def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")

    rezultat = [(ip, numar) for ip, numar in counts.items() if numar >= prag]
    rezultat.sort(key=lambda pereche: pereche[1], reverse=True)
    return rezultat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("log")
    parser.add_argument("--prag", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    esecuri = citeste_esecuri(args.log)
    counts = pe_ip(esecuri)
    try:
        adrese = suspecti(counts, args.prag)
    except ValueError as eroare:
        parser.error(str(eroare))

    if args.json:
        raport = {"esecuri": len(esecuri), "pe_ip": dict(counts), "suspecti": adrese}
        print(json.dumps(raport, indent=2))
        return

    print(f"Esecuri de autentificare: {len(esecuri)}")
    for ip, numar in counts.most_common():
        print(f"  {ip}: {numar}")
    print(f"Suspecti (prag {args.prag}):")
    for ip, numar in adrese:
        print(f"  {ip}  ({numar} incercari)  BRUTE FORCE")


if __name__ == "__main__":
    main()
