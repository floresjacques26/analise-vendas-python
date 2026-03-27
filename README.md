# Análise de Vendas — Loja de Eletrônicos (Brasil 2024)

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.x-green)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13-orange)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-red)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b)

> Análise exploratória de dados de vendas de eletrônicos no Brasil (2024) com Python, Pandas e Seaborn. Projeto de portfólio com foco em **tomada de decisão baseada em dados**.

## Dashboard Online

**[Acesse o dashboard interativo aqui](https://alexandre-sales-dashboard.streamlit.app/)**

---

## Resultados em Números

| Métrica | Valor |
|---------|-------|
| Receita Total | R$ 22.318.832 |
| Lucro Total | R$ 9.015.432 |
| Margem Média | 40,4% |
| Produto Líder | Smartphone (receita) |
| Maior Margem | Mouse Gamer (47%) |
| Melhor Trimestre | Q4 — 33% do faturamento |
| Região Líder | Sudeste — 42% das vendas |
| Total de Transações | 5.000 |

---

## Contexto

Uma loja de eletrônicos com atuação em todas as regiões do Brasil precisa orientar suas decisões estratégicas para 2025 com base em dados históricos de vendas do ano anterior.

---

## Objetivos

- Identificar quais produtos geram mais receita e lucro
- Detectar sazonalidade e os meses de pico de faturamento
- Comparar a performance comercial entre as regiões do país
- Encontrar os produtos com maior margem de lucro para priorização estratégica

---

## Metodologia

1. **Geração do dataset** — 5.000 transações **sintéticas criadas para fins educacionais/portfólio**, baseadas em padrões reais do varejo de eletrônicos brasileiro (sazonalidade Q4, concentração no Sudeste, mix de produtos)
2. **Limpeza e exploração** — verificação de tipos, valores nulos e distribuições com Pandas
3. **Análise por dimensão** — produto, mês e região, calculando receita, lucro e margem
4. **Visualização** — gráficos de barras, linhas, duplo eixo e heatmap com Matplotlib/Seaborn
5. **Interpretação de negócio** — tradução dos números em insights acionáveis

---

## Análises Realizadas

| # | Pergunta de Negócio | Técnica |
|---|---------------------|---------|
| 1 | Quais produtos vendem mais? | Agregação + ranking |
| 2 | Qual mês fatura mais? | Série temporal mensal |
| 3 | Qual região performa melhor? | Comparação multivariada |
| 4 | Quais produtos têm maior margem? | Cálculo de margem percentual |

---

## Visualizações

### Receita e Volume por Produto
![Produtos](assets/grafico_produtos.png)

### Sazonalidade Mensal
![Mensal](assets/grafico_mensal.png)

### Performance por Região
![Regioes](assets/grafico_regioes.png)

### Margem de Lucro por Produto
![Margem](assets/grafico_margem.png)

---

## Insights

| # | Insight | Impacto |
|---|---------|---------|
| 1 | **Smartphone é o campeão de receita** — maior volume com ticket médio-alto | Alto |
| 2 | **Q4 concentra ~33% do faturamento anual** — sazonalidade forte em Nov/Dez | Alto |
| 3 | **Sudeste representa 42% das vendas**, mas Norte e Nordeste têm margem similar | Médio |
| 4 | **Mouse Gamer e Teclado Mecânico têm as maiores margens** — produtos estratégicos | Alto |
| 5 | **Notebook lidera em receita absoluta**, mas margem está abaixo da média | Médio |

---

## Recomendações

- **Criar bundles de periféricos** (Mouse + Teclado + Headset): margens mais altas, ticket maior
- **Dobrar estoque em outubro** para capturar toda a demanda de Black Friday
- **Investir em distribuição no Norte e Nordeste**: crescimento com boa margem, base ainda pequena
- **Negociar condições com fornecedores de notebook**: produto de maior receita com margem abaixo da média

---

## Aplicação no Mundo Real

Este projeto representa uma solução aplicável por qualquer varejista de eletrônicos para:

| Área | Como este projeto ajuda |
|------|------------------------|
| **Estoque** | Saber quais produtos acumular e em qual trimestre |
| **Marketing** | Direcionar verba para regiões e produtos com maior retorno |
| **Financeiro** | Identificar onde a margem está sendo destruída |
| **Comercial** | Criar promoções no período certo (Q4) para maximizar receita |
| **Estratégia** | Priorizar expansão nas regiões com crescimento e boa margem |

---

## Etapas do Projeto

```
1. Coleta de dados          → dataset de 5.000 transações com padrões reais do varejo BR
2. Limpeza e tratamento     → tipagem, nulos, criação de campos derivados (lucro, margem)
3. Análise exploratória     → distribuições, correlações e agregações por dimensão
4. Visualização de dados    → 4 gráficos estratégicos com Matplotlib e Seaborn
5. Geração de insights      → tradução dos números em decisões de negócio
6. Dashboard interativo     → app Streamlit com filtros por região, categoria e período
```

---

## Próximos Passos

- [ ] Modelo de **previsão de vendas** por mês (Prophet ou ARIMA)
- [ ] Cruzar **ticket médio por região** com renda per capita do IBGE
- [ ] Calcular **LTV (lifetime value)** por categoria de produto
- [ ] Substituir dataset sintético por **dados reais** via API pública (ex: IBGE, Receita Federal)
- [ ] Adicionar **testes automatizados** para as funções de agregação e margem

---

## Estrutura do Projeto

```
analise-vendas-python/
├── assets/                     # Gráficos para o README
│   ├── grafico_produtos.png
│   ├── grafico_mensal.png
│   ├── grafico_regioes.png
│   └── grafico_margem.png
├── data/
│   └── vendas.csv              # Gerado automaticamente pelo notebook
├── notebook.ipynb              # Análise exploratória completa
├── app.py                      # Dashboard interativo (Streamlit)
├── gerar_graficos.py           # Script para regenerar os gráficos
├── requirements.txt
└── README.md
```

---

## Como Executar

### Jupyter Notebook (análise completa)
```bash
git clone https://github.com/floresjacques26/analise-vendas-python.git
cd analise-vendas-python
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

> Execute as células em ordem. A primeira célula gera `data/vendas.csv` automaticamente.

### Dashboard Streamlit (local)
```bash
streamlit run app.py
```

> O dashboard também está disponível online: **[alexandre-sales-dashboard.streamlit.app](https://alexandre-sales-dashboard.streamlit.app/)**

---

## Competências Demonstradas

- Análise exploratória de dados (EDA)
- Limpeza e transformação de dados com Pandas
- Visualização estratégica com Matplotlib e Seaborn
- Storytelling com dados — tradução de números em decisões
- Desenvolvimento de dashboard interativo com Streamlit
- Raciocínio de negócio aplicado a dados

---

## Stack

`Python 3.13` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `Jupyter Notebook` · `Streamlit`

---

## Autor

**Alexandre Flores Jacques**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin)](https://www.linkedin.com/in/alexandre-jacques-237857256/)
[![GitHub](https://img.shields.io/badge/GitHub-black?logo=github)](https://github.com/floresjacques26)
