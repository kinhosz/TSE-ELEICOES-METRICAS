# Seções eleitorais em que Lula teve de 0 a 10 votos — 2º turno 2026

Levantamento feito **somente com dados públicos do TSE**: todas as seções eleitorais do
2º turno para Presidente (25/10/2026, Lula × Flávio Bolsonaro) em que Lula recebeu entre
0 e 10 votos. Para cada seção mostramos local, endereço e os votos de Lula, de Flávio,
os brancos e os nulos.

- 📄 **Lista completa, agrupada pelos votos de Lula:** [SECOES.md](SECOES.md)
- 📊 **Planilha (CSV):** [secoes_lula_0a10_votos_turno2.csv](secoes_lula_0a10_votos_turno2.csv)
- 🖼️ **Imagens:** [instagram.png](instagram.png) (gráfico) e [instagram_detalhado.png](instagram_detalhado.png) (tabela 0 a 10)

## Resumo

De **499.205 seções** do 2º turno (Brasil + exterior), Lula teve de 0 a 10 votos em **227**.

| Votos de Lula na seção | Seções | Votos Lula | Votos Flávio | Brancos | Nulos | Total de votos |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 4 | 0 | 296 | 6 | 0 | 302 |
| 1 | 7 | 7 | 667 | 3 | 2 | 679 |
| 2 | 3 | 6 | 237 | 1 | 0 | 244 |
| 3 | 9 | 27 | 617 | 3 | 6 | 653 |
| 4 | 23 | 92 | 1.537 | 12 | 13 | 1.654 |
| 5 | 22 | 110 | 1.431 | 18 | 15 | 1.574 |
| 6 | 17 | 102 | 1.076 | 12 | 16 | 1.206 |
| 7 | 28 | 196 | 1.572 | 13 | 17 | 1.798 |
| 8 | 42 | 336 | 2.818 | 36 | 41 | 3.231 |
| 9 | 34 | 306 | 2.352 | 20 | 29 | 2.707 |
| 10 | 38 | 380 | 2.554 | 20 | 26 | 2.980 |
| **Total (0 a 10)** | **227** | **1.562** | **15.157** | **144** | **165** | **17.028** |

As 4 seções com **zero** votos para Lula:

| UF | Município | Zona | Seção | Local | Lula | Flávio | Total |
|---|---|---:|---:|---|---:|---:|---:|
| PA | Chaves | 17 | 41 | EMEIF José Valerio Rodrigues (Ilha Viçosa) | 0 | 48 | 49 |
| PA | Jacareacanga | 102 | 44 | EMEF Getúlio Vargas (Gleba São Benedito) | 0 | 50 | 50 |
| RS | Arroio do Padre | 34 | 433 | Antiga Escola Silveira Martins (Colônia Cerrito) | 0 | 116 | 118 |
| RS | Cândido Godói | 166 | 81 | Escola Sto Inácio (Linha Abrantes) | 0 | 82 | 85 |

### Para comparação

Rodando o mesmo filtro para Flávio (`--candidato 22`): ele teve de 0 a 10 votos em
**3.042 seções**, sendo **106 com zero votos**. Isso acontece com os dois candidatos.
São seções pequenas (presídios, unidades de internação, embaixadas, aldeias, comunidades
rurais) ou comunidades em que a votação é muito concentrada num só candidato.

## Como conferir

Qualquer pessoa pode conferir os números de cada seção de forma independente:

1. **Boletim de Urna (BU) da seção.** No site de resultados do TSE
   (<https://resultados.tse.jus.br>), use a consulta de Boletim de Urna e informe
   **UF, município, zona e seção** (as colunas da lista). O BU é o comprovante que a
   própria urna imprime ao fim da votação. O app oficial **Boletim na Mão** também lê
   o QR Code do BU impresso.
2. **Arquivo oficial completo.** Baixe a votação por seção do TSE (Portal de Dados
   Abertos, <https://dadosabertos.tse.jus.br>):
   <https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip>
   e, no CSV, filtre `NR_TURNO = 2`, `SG_UF`, `NM_MUNICIPIO`, `NR_ZONA` e `NR_SECAO`.
   - `NR_VOTAVEL` 13 = Lula, 22 = Flávio, 95 = branco, 96 = nulo.
   - ⚠️ **Quando o candidato tem 0 votos na seção, o TSE não grava nenhuma linha para ele.**
     Não adianta procurar `QT_VOTOS = 0`: se a seção tem linhas para Flávio/brancos/nulos
     mas nenhuma para o número 13, Lula teve 0 votos ali.
3. **Rodar os scripts deste repositório** (abaixo), que fazem exatamente isso.

## Como reproduzir

Requer Python 3 (e `matplotlib` só para a imagem).

```bash
python3 urnas_lula.py                  # baixa o arquivo do TSE (~240 MB) e filtra Lula 0–10
python3 urnas_lula.py --candidato 22   # mesmo filtro para Flávio (usado na comparação)
python3 gerar_relatorio.py             # gera SECOES.md, resumo.md e instagram.png
```

Outras faixas: `python3 urnas_lula.py --min 0 --max 0` (só seções com zero votos).

## Observações

- Fonte: TSE, *Votação por seção eleitoral*, eleição de 2026, arquivo gerado em 26/10/2026.
- UF `ZZ` = seções no exterior.
- “Total de votos” = Lula + Flávio + brancos + nulos na seção.
