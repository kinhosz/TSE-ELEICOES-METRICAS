#!/usr/bin/env python3
"""Gera o relatório público a partir dos CSVs produzidos por urnas_lula.py.

Saídas:
    SECOES.md           lista completa das seções, agrupada pelos votos de Lula (0 a 10)
    resumo.md           tabela-resumo por grupo + total geral
    instagram.png       imagem 1080x1350 para post (gráfico)
    instagram_detalhado.png  imagem 1080x1350 com a tabela 0 a 10

Uso:
    python3 urnas_lula.py && python3 urnas_lula.py --candidato 22
    python3 gerar_relatorio.py
"""
import csv
import collections

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

LULA_CSV = "secoes_lula_0a10_votos_turno2.csv"
FLAVIO_CSV = "secoes_flavio_0a10_votos_turno2.csv"
TOTAL_SECOES = 499_205  # seções do 2º turno no arquivo do TSE (impresso por urnas_lula.py)
NUM = ["lula", "flavio", "branco", "nulo", "total"]


def ler(path):
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    for r in rows:
        for k in NUM:
            r[k] = int(r[k])
    return rows


def fmt(n):
    return f"{n:,}".replace(",", ".")


def somar(rows):
    return {k: sum(r[k] for r in rows) for k in NUM}


def tabela_resumo(grupos, total):
    linhas = [
        "| Votos de Lula na seção | Seções | Votos Lula | Votos Flávio | Brancos | Nulos | Total de votos |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for v in range(11):
        rows = grupos.get(v, [])
        s = somar(rows)
        linhas.append(f"| {v} | {fmt(len(rows))} | {fmt(s['lula'])} | {fmt(s['flavio'])} | "
                      f"{fmt(s['branco'])} | {fmt(s['nulo'])} | {fmt(s['total'])} |")
    n = sum(len(r) for r in grupos.values())
    linhas.append(f"| **Total (0 a 10)** | **{fmt(n)}** | **{fmt(total['lula'])}** | **{fmt(total['flavio'])}** | "
                  f"**{fmt(total['branco'])}** | **{fmt(total['nulo'])}** | **{fmt(total['total'])}** |")
    return "\n".join(linhas)


def gerar_secoes_md(grupos, total):
    out = [
        "# Seções em que Lula teve de 0 a 10 votos — 2º turno 2026 (Presidente)",
        "",
        "Fonte: TSE, Dados Abertos — votação por seção eleitoral (arquivo gerado em 26/10/2026).",
        "Para conferir cada seção, veja o [README](README.md#como-conferir).",
        "",
        "## Resumo",
        "",
        tabela_resumo(grupos, total),
        "",
    ]
    for v in range(11):
        rows = grupos.get(v, [])
        s = somar(rows)
        out += [
            f"## Lula com {v} voto{'s' if v != 1 else ''} — {fmt(len(rows))} seç{'ões' if len(rows) != 1 else 'ão'}",
            "",
            "| UF | Município | Zona | Seção | Local de votação | Endereço | Lula | Flávio | Brancos | Nulos | Total |",
            "|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|",
        ]
        for r in rows:
            out.append(f"| {r['uf']} | {r['municipio']} | {r['zona']} | {r['secao']} | {r['local']} | "
                       f"{r['endereco']} | {r['lula']} | {r['flavio']} | {r['branco']} | {r['nulo']} | {r['total']} |")
        out += [
            f"| | **Subtotal** | | | | | **{fmt(s['lula'])}** | **{fmt(s['flavio'])}** | "
            f"**{fmt(s['branco'])}** | **{fmt(s['nulo'])}** | **{fmt(s['total'])}** |",
            "",
        ]
    out += [
        "## Total geral (todas as seções acima)",
        "",
        f"- Seções: **{fmt(sum(len(r) for r in grupos.values()))}**",
        f"- Votos Lula: **{fmt(total['lula'])}**",
        f"- Votos Flávio: **{fmt(total['flavio'])}**",
        f"- Brancos: **{fmt(total['branco'])}** · Nulos: **{fmt(total['nulo'])}**",
        f"- Total de votos nessas seções: **{fmt(total['total'])}**",
        "",
        "UF `ZZ` = seções no exterior.",
        "",
    ]
    with open("SECOES.md", "w", encoding="utf-8") as f:
        f.write("\n".join(out))


def gerar_imagem(grupos, total, flavio_rows):
    surface, ink, ink2, muted, bar = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#2a78d6"
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100, facecolor=surface)

    n = sum(len(r) for r in grupos.values())
    fig.text(0.07, 0.94, "Seções em que Lula teve de 0 a 10 votos", fontsize=30, weight="bold", color=ink)
    fig.text(0.07, 0.905, f"2º turno 2026 · Presidente · {fmt(TOTAL_SECOES)} seções no Brasil e exterior",
             fontsize=17, color=ink2)

    # Números de destaque
    tiles = [(fmt(n), "seções"), (fmt(total["lula"]), "votos Lula"), (fmt(total["flavio"]), "votos Flávio")]
    for i, (valor, rotulo) in enumerate(tiles):
        x = 0.07 + i * 0.31
        fig.text(x, 0.80, valor, fontsize=46, weight="bold", color=ink)
        fig.text(x, 0.77, rotulo, fontsize=18, color=ink2)
    fig.text(0.07, 0.735, "somando todas essas seções", fontsize=15, color=muted)

    # Barras: nº de seções por votos de Lula
    ax = fig.add_axes([0.10, 0.32, 0.83, 0.35], facecolor=surface)
    xs = list(range(11))
    ys = [len(grupos.get(v, [])) for v in xs]
    bars = ax.bar(xs, ys, width=0.72, color=bar, edgecolor=surface, linewidth=2)
    for b, y in zip(bars, ys):
        ax.text(b.get_x() + b.get_width() / 2, y + 0.8, str(y), ha="center", va="bottom", fontsize=15, color=ink)
    ax.set_xticks(xs)
    ax.tick_params(axis="x", labelsize=16, colors=ink2, length=0)
    ax.tick_params(axis="y", labelsize=13, colors=muted, length=0)
    ax.set_xlabel("votos de Lula na seção", fontsize=17, color=ink2, labelpad=10)
    ax.set_ylabel("número de seções", fontsize=15, color=muted)
    ax.grid(axis="y", color="#e6e5e1", linewidth=1)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#c9c8c3")
    ax.set_ylim(0, max(ys) * 1.15)

    # Contexto e fonte
    zero_f = sum(1 for r in flavio_rows if r["flavio"] == 0)
    fig.text(0.07, 0.15,
             f"Para comparação: Flávio teve de 0 a 10 votos em {fmt(len(flavio_rows))} seções\n"
             f"(em {fmt(zero_f)} delas, zero). Seções pequenas e comunidades homogêneas\n"
             "concentram votos assim, para os dois lados.",
             fontsize=16, color=ink2, linespacing=1.5)
    fig.text(0.07, 0.07,
             "Fonte: TSE — Dados Abertos, votação por seção eleitoral (26/10/2026)\n"
             "Lista completa e como conferir cada seção: link na bio",
             fontsize=14, color=muted, linespacing=1.5)

    fig.savefig("instagram.png", facecolor=surface)


def gerar_imagem_tabela(grupos, total):
    surface, ink, ink2, muted, rule = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100, facecolor=surface)

    fig.text(0.07, 0.94, "Detalhado: Lula de 0 a 10 votos", fontsize=30, weight="bold", color=ink)
    fig.text(0.07, 0.905, "2º turno 2026 · Presidente · soma dos votos nas seções de cada grupo",
             fontsize=17, color=ink2)

    cols = [("Votos Lula\nna seção", 0.07, "left"), ("Seções", 0.40, "right"), ("Votos\nLula", 0.56, "right"),
            ("Votos\nFlávio", 0.74, "right"), ("Total de\nvotos", 0.93, "right")]
    y = 0.84
    for titulo, x, ha in cols:
        fig.text(x, y, titulo, fontsize=16, color=muted, ha=ha, va="center", linespacing=1.3)
    y -= 0.04
    fig.add_artist(plt.Line2D([0.07, 0.93], [y, y], color="#c9c8c3", linewidth=1.5))

    passo = 0.052
    linhas = []
    for v in range(11):
        rows = grupos.get(v, [])
        s = somar(rows)
        linhas.append((str(v), fmt(len(rows)), fmt(s["lula"]), fmt(s["flavio"]), fmt(s["total"]), "normal"))
    n = sum(len(r) for r in grupos.values())
    linhas.append(("Total", fmt(n), fmt(total["lula"]), fmt(total["flavio"]), fmt(total["total"]), "bold"))

    for i, linha in enumerate(linhas):
        y -= passo
        if linha[-1] == "bold":
            fig.add_artist(plt.Line2D([0.07, 0.93], [y + passo / 2, y + passo / 2], color="#c9c8c3", linewidth=1.5))
        elif i:
            fig.add_artist(plt.Line2D([0.07, 0.93], [y + passo / 2, y + passo / 2], color=rule, linewidth=1))
        for (_, x, ha), valor in zip(cols, linha[:5]):
            fig.text(x, y, valor, fontsize=21, color=ink, ha=ha, va="center", weight=linha[-1])

    fig.text(0.07, 0.06,
             "“Total de votos” inclui brancos e nulos.\n"
             "Fonte: TSE — Dados Abertos, votação por seção eleitoral (26/10/2026)\n"
             "Lista completa com locais e como conferir cada seção: link na bio",
             fontsize=14, color=muted, linespacing=1.5)

    fig.savefig("instagram_detalhado.png", facecolor=surface)


def main():
    lula = ler(LULA_CSV)
    flavio = ler(FLAVIO_CSV)
    grupos = collections.defaultdict(list)
    for r in lula:
        grupos[r["lula"]].append(r)
    total = somar(lula)

    gerar_secoes_md(grupos, total)
    with open("resumo.md", "w", encoding="utf-8") as f:
        f.write(tabela_resumo(grupos, total) + "\n")
    gerar_imagem(grupos, total, flavio)
    gerar_imagem_tabela(grupos, total)
    print(tabela_resumo(grupos, total))


if __name__ == "__main__":
    main()
