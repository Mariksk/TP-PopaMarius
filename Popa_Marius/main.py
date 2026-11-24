from httptools import PATHS, report


def main():
    rezultate = []
    for cale in PATHS:
        pagina = report(cale)
        pagina["path"] = cale
        rezultate.append(pagina)

    reusite = [pagina for pagina in rezultate if pagina["status"] == 200]
    reusite.sort(key=lambda pagina: pagina["seconds"], reverse=True)
    for pagina in reusite:
        print(f"{pagina['path']} -> 200, {pagina['seconds']:.2f} secunde")
    print(f"Reușite: {len(reusite)} | Eșuate: {len(rezultate) - len(reusite)}")


if __name__ == "__main__":
    main()
