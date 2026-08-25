# Painel Mini FMH

Dashboard estático (HTML/SVG puro, sem dependências) para análise comparativa dos
indicadores operacionais **Mini FMH**, a partir da aba **daily** da planilha *Mini FMH*.

**Site:** publicado no Vercel (deploy estático).

## O que o painel faz

- **Indicadores** (Metric) — seleção múltipla das 31 métricas.
- **Operações** (Hub name) — seleção múltipla dos hubs + linha *Overall* agregada.
- **Tipo** (Mini FMH) — filtro *Todos / Mini FMH / Demais*.
- **Mês** — *Tudo / Junho / … / Outubro* (período dos dados: 01/jun–02/out 2025).
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
data/daily.json       # dados já tratados e embutidos no index.html
data/daily.csv        # export bruto da aba daily (referência)
scripts/build.py      # gera o index.html a partir de data/daily.json
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

Aba **daily** de *Mini FMH* (Google Sheets). Metric = indicador, Hub name = operação,
Regional por hub, datas diárias no cabeçalho. Período: 01/jun–02/out 2025 (colunas
semanais/mensais de forecast são ignoradas). Os 12 hubs Mini FMH são marcados por lista conhecida.
