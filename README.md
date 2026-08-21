# Painel Mini FMH

Dashboard estático (HTML/SVG puro, sem dependências) para análise comparativa dos
indicadores operacionais **Mini FMH**, a partir da aba **Página10** da planilha
*Mini FMH - Analysis*.

**Site:** publicado no Vercel (deploy estático).

## O que o painel faz

- **Indicadores** (coluna A da Página10) — seleção múltipla das 31 métricas.
- **Operações** (coluna D) — seleção múltipla dos hubs + linha *Overall* agregada.
- **Tipo** (coluna E) — filtro *Todos / Mini FMH / Demais*.
- **Mês** — *Tudo / Junho / Julho* (período dos dados: 01/jun–31/jul 2025).
- **Visões de gráfico**, pensadas para comparar operações sem poluição visual:
  - **Ranking** — quem está na frente/atrás; marca melhor/pior quando é um só indicador.
  - **Linha suavizada** — média móvel de 7 dias (remove o serrilhado de fim de semana).
  - **Pequenos múltiplos** — um mini-gráfico por operação, mesma escala.
  - **Mapa de calor** — operações × dias.
  - **Linha diária** — série crua.
- KPIs, resumo por série e tabela diária completa.

## Estrutura

```
index.html            # dashboard final (gerado; dados embutidos, self-contained)
data/pagina10.json    # dados já tratados e embutidos no index.html
data/pagina10.csv     # export bruto da aba Página10 (referência)
scripts/build.py      # gera o index.html a partir de data/pagina10.json
vercel.json           # configuração de deploy estático
```

## Regenerar o `index.html`

```bash
python3 scripts/build.py
```

## Deploy no Vercel

Projeto 100% estático — sem build step. No Vercel:

1. **Add New… → Project** e importe este repositório do GitHub.
2. **Framework Preset:** `Other`.
3. **Build Command:** deixe vazio · **Output Directory:** `.` (raiz).
4. **Deploy.**

A cada `push` na branch conectada, o Vercel republica automaticamente.

## Fonte dos dados

Aba **Página10** de *Mini FMH - Analysis* (Google Sheets). Coluna A = indicador,
coluna D = operação, coluna E = tipo (Mini FMH), cabeçalho F3:EC3 = datas.
Período disponível: junho e julho de 2025.
