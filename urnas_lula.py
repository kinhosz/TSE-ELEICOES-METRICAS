#!/usr/bin/env python3
"""Seções eleitorais em que um candidato teve poucos votos (2º turno 2026, Presidente).

Fonte: TSE - Dados Abertos, "Votação por seção eleitoral"
https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip

Obs.: o arquivo do TSE não traz linha para candidato com 0 votos na seção;
esses zeros são reconstruídos a partir das demais linhas da seção.

Uso:
    python3 urnas_lula.py                 # Lula, 0 a 10 votos
    python3 urnas_lula.py --candidato 22  # Flávio Bolsonaro
    python3 urnas_lula.py --min 0 --max 0
"""
import argparse
import collections
import csv
import io
import os
import sys
import urllib.request
import zipfile

URL = "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip"
CSV_NAME = "votacao_secao_2026_BR.csv"
NOMES = {"13": "LULA", "22": "FLAVIO", "95": "BRANCO", "96": "NULO"}


def baixar(destino):
    if os.path.exists(destino):
        return
    print(f"Baixando {URL} (~240 MB)...", file=sys.stderr)
    urllib.request.urlretrieve(URL, destino + ".part")
    os.replace(destino + ".part", destino)


def ler_secoes(zip_path, turno):
    secoes = {}
    with zipfile.ZipFile(zip_path) as z, z.open(CSV_NAME) as raw:
        reader = csv.DictReader(io.TextIOWrapper(raw, encoding="latin1", newline=""), delimiter=";")
        for row in reader:
            if row["NR_TURNO"] != turno or row["CD_CARGO"] != "1":
                continue
            chave = (row["SG_UF"], row["CD_MUNICIPIO"], row["NR_ZONA"], row["NR_SECAO"])
            sec = secoes.get(chave)
            if sec is None:
                sec = secoes[chave] = {
                    "uf": row["SG_UF"],
                    "municipio": row["NM_MUNICIPIO"],
                    "zona": row["NR_ZONA"],
                    "secao": row["NR_SECAO"],
                    "local": row["NM_LOCAL_VOTACAO"],
                    "endereco": row["DS_LOCAL_VOTACAO_ENDERECO"],
                    "votos": collections.Counter(),
                }
            sec["votos"][row["NR_VOTAVEL"]] += int(row["QT_VOTOS"])
    return secoes


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--candidato", default="13", help="número do candidato (13=Lula, 22=Flávio)")
    p.add_argument("--min", type=int, default=0)
    p.add_argument("--max", type=int, default=10)
    p.add_argument("--turno", default="2")
    p.add_argument("--zip", default="votacao_secao_2026_BR.zip", help="cache local do arquivo do TSE")
    p.add_argument("--saida", default=None, help="CSV de saída")
    args = p.parse_args()

    baixar(args.zip)
    secoes = ler_secoes(args.zip, args.turno)

    filtradas = [s for s in secoes.values() if args.min <= s["votos"][args.candidato] <= args.max]
    filtradas.sort(key=lambda s: (s["votos"][args.candidato], s["uf"], s["municipio"], int(s["zona"]), int(s["secao"])))

    nome = NOMES.get(args.candidato, args.candidato)
    saida = args.saida or f"secoes_{nome.lower()}_{args.min}a{args.max}_votos_turno{args.turno}.csv"
    campos = ["uf", "municipio", "zona", "secao", "local", "endereco", "lula", "flavio", "branco", "nulo", "total"]
    with open(saida, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(campos)
        for s in filtradas:
            v = s["votos"]
            w.writerow([s["uf"], s["municipio"], s["zona"], s["secao"], s["local"], s["endereco"],
                        v["13"], v["22"], v["95"], v["96"], sum(v.values())])

    # Resumo
    print(f"Seções no {args.turno}º turno: {len(secoes):,}")
    print(f"Seções com {nome} entre {args.min} e {args.max} votos: {len(filtradas):,}")
    print("\nPor quantidade de votos do candidato:")
    for k, n in sorted(collections.Counter(s["votos"][args.candidato] for s in filtradas).items()):
        print(f"  {k:>3} votos: {n:,} seções")
    print("\nPor UF:")
    for uf, n in collections.Counter(s["uf"] for s in filtradas).most_common():
        print(f"  {uf}: {n:,}")
    print("\nTotal de votos na seção (todas as opções), nas seções filtradas:")
    faixas = [(0, 20), (21, 50), (51, 100), (101, 200), (201, 10**9)]
    for a, b in faixas:
        n = sum(1 for s in filtradas if a <= sum(s["votos"].values()) <= b)
        print(f"  {a}-{b if b < 10**9 else '+'}: {n:,}")
    print(f"\nArquivo detalhado: {saida}")


if __name__ == "__main__":
    main()
