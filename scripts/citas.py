"""Papers que citan a uno dado, vía OpenAlex (sin API key).

Uso: python3 citas.py <DOI> ["términos de búsqueda"] [--n 15] [--orden fecha|citas]
Imprime año, citas, DOI, título y el abstract (recortado) de cada paper que lo cita.
"""
import argparse
import json
import subprocess
import urllib.parse

API = "https://api.openalex.org"


def get(url):
    # curl y no urllib: el Python de python.org en macOS no trae certificados raíz
    return json.loads(subprocess.run(["curl", "-sfL", "-m", "30", url], check=True,
                                     capture_output=True, text=True).stdout)


def abstract(w, largo=600):
    inv = w.get("abstract_inverted_index") or {}
    palabras = sorted((i, p) for p, idx in inv.items() for i in idx)
    texto = " ".join(p for _, p in palabras).removeprefix("Abstract ")
    return (texto[:largo] + "…") if len(texto) > largo else texto or "(sin abstract en OpenAlex)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doi")
    ap.add_argument("terminos", nargs="?", default="")
    ap.add_argument("--n", type=int, default=15)
    ap.add_argument("--orden", choices=["fecha", "citas"], default="fecha")
    a = ap.parse_args()

    doi = a.doi.removeprefix("https://doi.org/")
    paper = get(f"{API}/works/doi:{urllib.parse.quote(doi)}?select=id,title,cited_by_count")
    wid = paper["id"].rsplit("/", 1)[-1]
    filtro = f"cites:{wid}"
    if a.terminos:
        filtro += f",title_and_abstract.search:{a.terminos}"
    orden = "publication_date:desc" if a.orden == "fecha" else "cited_by_count:desc"
    q = urllib.parse.urlencode({"filter": filtro, "sort": orden, "per-page": a.n,
                                "select": "title,publication_year,doi,cited_by_count,abstract_inverted_index"})
    res = get(f"{API}/works?{q}")

    print(f"# {paper['title']} — citado {paper['cited_by_count']} veces; "
          f"{res['meta']['count']} coinciden con el filtro\n")
    for w in res["results"]:
        print(f"## {w['publication_year']} · {w['cited_by_count']} citas · {w['doi']}\n{w['title']}\n{abstract(w)}\n")


if __name__ == "__main__":
    main()
