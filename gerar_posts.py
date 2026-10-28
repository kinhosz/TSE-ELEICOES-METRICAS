#!/usr/bin/env python3
"""Gera o carrossel do Instagram (1080x1350) em posts/.

Usa os CSVs de urnas_lula.py e as imagens de gerar_relatorio.py (slides 2 e 3).

Uso:
    python3 gerar_relatorio.py && python3 gerar_posts.py
"""
import os
import shutil

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from gerar_relatorio import FLAVIO_CSV, LULA_CSV, TOTAL_SECOES, fmt, ler, somar  # noqa: E402

SURFACE, INK, INK2, MUTED, RULE, CARD, ACCENT = (
    "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1", "#f1f0ec", "#2a78d6")
REPO = "github.com/kinhosz/TSE-ELEICOES-METRICAS"
N_SLIDES = 7
OUT = "posts"


def novo_slide(n):
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100, facecolor=SURFACE)
    fig.text(0.07, 0.035, "Fonte: TSE — Dados Abertos (26/10/2026)", fontsize=13, color=MUTED)
    fig.text(0.93, 0.035, f"{n}/{N_SLIDES}", fontsize=13, color=MUTED, ha="right")
    return fig


def card(fig, x, y, w, h):
    fig.add_artist(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.015",
                                  transform=fig.transFigure, facecolor=CARD, edgecolor="none"))


def nome_proprio(txt):
    return " ".join(w if i == 0 or w not in ("Do", "Da", "De", "Dos", "Das") else w.lower()
                    for i, w in enumerate(txt.title().split()))


def pct(n):
    return f"{n / TOTAL_SECOES * 100:.2f}%".replace(".", ",")


def salvar(fig, nome):
    fig.savefig(os.path.join(OUT, nome), facecolor=SURFACE)
    plt.close(fig)


def capa(lula, total):
    fig = novo_slide(1)
    fig.text(0.07, 0.86, "ELEIÇÕES 2026 · 2º TURNO · PRESIDENTE", fontsize=17, color=ACCENT, weight="bold")
    fig.text(0.07, 0.72, "Em quantas urnas\nLula teve de 0 a 10\nvotos?", fontsize=52, weight="bold",
             color=INK, va="top", linespacing=1.15)
    fig.text(0.07, 0.36, fmt(len(lula)), fontsize=150, weight="bold", color=INK)
    fig.text(0.07, 0.30, f"seções, de {fmt(TOTAL_SECOES)} no Brasil e exterior", fontsize=24, color=INK2)
    fig.text(0.07, 0.17, f"Nelas: {fmt(total['lula'])} votos para Lula e {fmt(total['flavio'])} para Flávio.\n"
             "Arraste para ver os dados →", fontsize=19, color=INK2, linespacing=1.6)
    salvar(fig, "01_capa.png")


def zeros(lula):
    fig = novo_slide(4)
    zs = [r for r in lula if r["lula"] == 0]
    fig.text(0.07, 0.92, f"As {len(zs)} seções com zero votos", fontsize=36, weight="bold", color=INK)
    fig.text(0.07, 0.885, "para Lula no 2º turno", fontsize=20, color=INK2)
    h, gap, y = 0.165, 0.02, 0.85
    for r in zs:
        y -= h
        card(fig, 0.07, y, 0.86, h)
        fig.text(0.10, y + h - 0.035, f"{nome_proprio(r['municipio'])} — {r['uf']}", fontsize=24, weight="bold", color=INK)
        fig.text(0.10, y + h - 0.07, r["local"].title(), fontsize=16, color=INK2)
        fig.text(0.10, y + h - 0.097, f"Zona {r['zona']} · Seção {r['secao']}", fontsize=15, color=MUTED)
        fig.text(0.10, y + 0.025, f"Lula {r['lula']}", fontsize=22, weight="bold", color=INK)
        fig.text(0.30, y + 0.025, f"Flávio {r['flavio']}", fontsize=22, weight="bold", color=INK)
        fig.text(0.90, y + 0.025, f"{r['total']} votos na seção", fontsize=16, color=INK2, ha="right")
        y -= gap
    fig.text(0.07, 0.075, "São seções pequenas, em áreas rurais e ribeirinhas.", fontsize=16, color=INK2)
    salvar(fig, "04_zero_votos.png")


def contexto(lula, flavio):
    fig = novo_slide(5)
    fig.text(0.07, 0.92, "E o Flávio?", fontsize=40, weight="bold", color=INK)
    fig.text(0.07, 0.88, "O mesmo filtro, aplicado aos dois candidatos", fontsize=20, color=INK2)
    zl = sum(1 for r in lula if r["lula"] == 0)
    zf = sum(1 for r in flavio if r["flavio"] == 0)
    for i, (nome, n, z) in enumerate([("Lula", len(lula), zl), ("Flávio", len(flavio), zf)]):
        x = 0.07 + i * 0.445
        card(fig, x, 0.50, 0.415, 0.33)
        fig.text(x + 0.03, 0.775, f"{nome} com 0 a 10 votos", fontsize=19, color=INK2)
        fig.text(x + 0.03, 0.66, fmt(n), fontsize=72, weight="bold", color=INK)
        fig.text(x + 0.03, 0.625, "seções", fontsize=18, color=INK2)
        fig.text(x + 0.03, 0.54, f"{fmt(z)} com zero votos", fontsize=19, weight="bold", color=INK)
    fig.text(0.07, 0.42, "Por que isso acontece?", fontsize=26, weight="bold", color=INK)
    fig.text(0.07, 0.40,
             "• Seções pequenas: presídios, unidades de internação,\n"
             "  embaixadas, aldeias e comunidades isoladas.\n"
             "• Comunidades homogêneas, onde quase todo mundo\n"
             "  vota no mesmo candidato.\n"
             f"• É raro: {fmt(len(lula))} de {fmt(TOTAL_SECOES)} seções "
             f"({pct(len(lula))}) para Lula,\n"
             f"  {fmt(len(flavio))} ({pct(len(flavio))}) para Flávio.",
             fontsize=19, color=INK2, va="top", linespacing=1.6)
    salvar(fig, "05_comparacao.png")


def conferir():
    fig = novo_slide(6)
    fig.text(0.07, 0.92, "Confira você mesmo", fontsize=40, weight="bold", color=INK)
    fig.text(0.07, 0.88, "Todos os dados são públicos", fontsize=20, color=INK2)
    passos = [
        ("1", "Boletim de Urna", "Em resultados.tse.jus.br, consulte o boletim\n"
                                 "informando UF, município, zona e seção.\nOu leia o QR Code com o app Boletim na Mão."),
        ("2", "Arquivo oficial do TSE", "Dados Abertos → votação por seção eleitoral 2026.\n"
                                        "Lula = 13, Flávio = 22. Sem linha do 13\nna seção = Lula teve 0 votos."),
        ("3", "Lista completa + código", f"Todas as {fmt(227)} seções, com local e endereço,\n"
                                         f"e o script que gera os números:\n{REPO}"),
    ]
    y = 0.84
    for num, titulo, texto in passos:
        h = 0.2
        y -= h
        card(fig, 0.07, y, 0.86, h)
        fig.text(0.11, y + h - 0.055, num, fontsize=44, weight="bold", color=ACCENT, va="center")
        fig.text(0.20, y + h - 0.045, titulo, fontsize=24, weight="bold", color=INK, va="center")
        fig.text(0.20, y + h - 0.08, texto, fontsize=16, color=INK2, va="top", linespacing=1.5)
        y -= 0.03
    fig.text(0.07, 0.09, "Link na bio.", fontsize=19, weight="bold", color=INK)
    salvar(fig, "06_como_conferir.png")


def encerramento(lula, total):
    fig = novo_slide(7)
    fig.text(0.07, 0.86, "RESUMO", fontsize=17, color=ACCENT, weight="bold")
    fig.text(0.07, 0.80, "Lula teve de 0 a 10 votos em\n"
             f"{fmt(len(lula))} das {fmt(TOTAL_SECOES)} seções.", fontsize=38, weight="bold",
             color=INK, va="top", linespacing=1.25)
    fig.text(0.07, 0.62, f"Somando essas seções: {fmt(total['lula'])} votos para Lula\n"
             f"e {fmt(total['flavio'])} para Flávio, de {fmt(total['total'])} votos.\n\n"
             "O mesmo acontece com Flávio, em mais seções.\n"
             "Não tire conclusões de uma urna isolada: confira a fonte.",
             fontsize=21, color=INK2, va="top", linespacing=1.6)
    card(fig, 0.07, 0.17, 0.86, 0.17)
    fig.text(0.10, 0.29, "Dados, lista completa e código", fontsize=22, weight="bold", color=INK)
    fig.text(0.10, 0.245, REPO, fontsize=19, color=ACCENT)
    fig.text(0.10, 0.20, "Link na bio · Compartilhe com quem viu a notícia", fontsize=17, color=INK2)
    salvar(fig, "07_encerramento.png")


def main():
    os.makedirs(OUT, exist_ok=True)
    lula, flavio = ler(LULA_CSV), ler(FLAVIO_CSV)
    total = somar(lula)
    capa(lula, total)
    shutil.copy("instagram.png", os.path.join(OUT, "02_grafico.png"))
    shutil.copy("instagram_detalhado.png", os.path.join(OUT, "03_tabela.png"))
    zeros(lula)
    contexto(lula, flavio)
    conferir()
    encerramento(lula, total)
    print("\n".join(sorted(os.listdir(OUT))))


if __name__ == "__main__":
    main()
