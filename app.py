"""
Dashboard interativo de Análise de Vendas — Loja de Eletrônicos (Brasil 2024)
Execute com: streamlit run app.py
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Análise de Vendas 2024",
    page_icon="📊",
    layout="wide",
)
sns.set_theme(style="whitegrid")


@st.cache_data
def carregar_dados():
    csv_path = Path("data/vendas.csv")
    if not csv_path.exists():
        Path("data").mkdir(exist_ok=True)
        np.random.seed(42)
        N = 5000
        produtos_info = {
            'Notebook':         ('Computadores', 2800, 1750),
            'Smartphone':       ('Celulares',    1900, 1150),
            'Tablet':           ('Celulares',    1300,  800),
            'Monitor':          ('Computadores',  900,  530),
            'Teclado Mecânico': ('Periféricos',   380,  190),
            'Mouse Gamer':      ('Periféricos',   290,  130),
            'Headset':          ('Periféricos',   470,  240),
            'Webcam':           ('Periféricos',   330,  170),
            'Impressora':       ('Computadores',  650,  410),
            'Roteador':         ('Redes',         260,  140),
        }
        regioes      = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
        pesos_regiao = [0.08, 0.18, 0.12, 0.42, 0.20]
        pesos_mes    = [0.055,0.050,0.070,0.070,0.080,0.080,0.080,0.090,0.090,0.100,0.115,0.120]
        produtos     = list(produtos_info.keys())
        pesos_prod   = [0.12,0.18,0.10,0.08,0.12,0.15,0.10,0.07,0.05,0.03]
        prod_col     = np.random.choice(produtos, N, p=pesos_prod)
        mes_col      = np.random.choice(range(1,13), N, p=pesos_mes)
        dia_col      = np.random.randint(1, 28, N)
        regiao_col   = np.random.choice(regioes, N, p=pesos_regiao)
        qtd_col      = np.random.randint(1, 8, N)
        cats, precos, custos = [], [], []
        for p in prod_col:
            cat, pb, cb = produtos_info[p]
            cats.append(cat)
            precos.append(round(pb * np.random.uniform(0.92, 1.08), 2))
            custos.append(round(cb * np.random.uniform(0.92, 1.08), 2))
        precos, custos = np.array(precos), np.array(custos)
        df = pd.DataFrame({
            'data':           pd.to_datetime({'year':2024,'month':mes_col,'day':dia_col}),
            'mes':            mes_col,
            'produto':        prod_col,
            'categoria':      cats,
            'regiao':         regiao_col,
            'quantidade':     qtd_col,
            'preco_unitario': precos,
            'custo_unitario': custos,
            'receita':        (qtd_col * precos).round(2),
            'lucro':          (qtd_col * (precos - custos)).round(2),
        })
        df.to_csv(csv_path, index=False)
    else:
        df = pd.read_csv(csv_path, parse_dates=['data'])
    return df


df_full = carregar_dados()
nomes_mes = {1:'Jan',2:'Fev',3:'Mar',4:'Abr',5:'Mai',6:'Jun',
             7:'Jul',8:'Ago',9:'Set',10:'Out',11:'Nov',12:'Dez'}

# ── Navegação ─────────────────────────────────────────────────────────────────
pagina = st.sidebar.radio(
    "Navegação",
    ["Visão Geral", "Análise por Produto"],
    index=0,
)
st.sidebar.divider()

# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA 1 — VISÃO GERAL
# ═════════════════════════════════════════════════════════════════════════════
if pagina == "Visão Geral":

    # Filtros
    st.sidebar.subheader("Filtros")
    regioes_sel = st.sidebar.multiselect(
        "Região", sorted(df_full['regiao'].unique()), default=sorted(df_full['regiao'].unique()))
    cats_sel = st.sidebar.multiselect(
        "Categoria", sorted(df_full['categoria'].unique()), default=sorted(df_full['categoria'].unique()))
    mes_range = st.sidebar.select_slider(
        "Período", options=list(range(1,13)), value=(1,12),
        format_func=lambda m: nomes_mes[m])

    df = df_full[
        df_full['regiao'].isin(regioes_sel) &
        df_full['categoria'].isin(cats_sel) &
        df_full['mes'].between(mes_range[0], mes_range[1])
    ]

    # Header
    st.title("📊 Análise de Vendas — Eletrônicos Brasil 2024")
    st.caption(f"{len(df):,} transações exibidas com os filtros selecionados.")

    # KPIs
    receita = df['receita'].sum()
    lucro   = df['lucro'].sum()
    margem  = lucro / receita * 100 if receita else 0
    ticket  = receita / len(df) if len(df) else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Receita Total",  f"R$ {receita:,.0f}")
    c2.metric("Lucro Total",    f"R$ {lucro:,.0f}")
    c3.metric("Margem Média",   f"{margem:.1f}%")
    c4.metric("Ticket Médio",   f"R$ {ticket:,.0f}")
    st.divider()

    # Produtos
    st.subheader("Por Produto")
    ca, cb = st.columns(2)

    with ca:
        fig, ax = plt.subplots(figsize=(8, 5))
        rp = df.groupby('produto')['receita'].sum().sort_values()
        rp.plot(kind='barh', ax=ax, color=sns.color_palette('Blues', len(rp)))
        ax.set_title('Receita por Produto', fontweight='bold')
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'R$ {x/1e6:.1f}M'))
        for i, v in enumerate(rp.values):
            ax.text(v + rp.max()*0.01, i, f'R$ {v/1e6:.2f}M', va='center', fontsize=9)
        plt.tight_layout(); st.pyplot(fig); plt.close()

    with cb:
        fig, ax = plt.subplots(figsize=(8, 5))
        mp = df.groupby('produto').apply(
            lambda x: x['lucro'].sum()/x['receita'].sum()*100).sort_values(ascending=False)
        med = mp.mean()
        mp.plot(kind='bar', ax=ax,
                color=['seagreen' if v >= med else 'tomato' for v in mp], edgecolor='white')
        ax.axhline(med, color='navy', linestyle='--', linewidth=1.5, label=f'Média: {med:.1f}%')
        ax.set_title('Margem de Lucro por Produto', fontweight='bold')
        ax.set_ylabel('Margem (%)'); ax.legend()
        plt.xticks(rotation=30, ha='right'); plt.tight_layout(); st.pyplot(fig); plt.close()

    st.divider()

    # Mensal
    st.subheader("Sazonalidade Mensal")
    mensal = df.groupby('mes').agg(receita=('receita','sum'), lucro=('lucro','sum')).reset_index()
    mensal['mes_nome'] = mensal['mes'].map(nomes_mes)
    mensal['margem']   = mensal['lucro'] / mensal['receita'] * 100

    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    x, w = np.arange(len(mensal)), 0.38
    axes[0].bar(x-w/2, mensal['receita']/1e3, w, label='Receita', color='steelblue', alpha=0.85)
    axes[0].bar(x+w/2, mensal['lucro']/1e3,   w, label='Lucro',   color='seagreen',  alpha=0.85)
    axes[0].set_xticks(x); axes[0].set_xticklabels(mensal['mes_nome'])
    axes[0].set_title('Receita e Lucro Mensal (R$ mil)', fontweight='bold'); axes[0].legend()
    axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f'R$ {v:.0f}k'))

    axes[1].plot(mensal['mes_nome'], mensal['margem'], marker='o', color='darkorange',
                 linewidth=2.5, markersize=9)
    axes[1].fill_between(range(len(mensal)), mensal['margem'], alpha=0.15, color='darkorange')
    axes[1].axhline(mensal['margem'].mean(), color='navy', linestyle='--', linewidth=1.5,
                    label=f'Média: {mensal["margem"].mean():.1f}%')
    for i, m in enumerate(mensal['margem']):
        axes[1].text(i, m + 0.3, f'{m:.1f}%', ha='center', fontsize=9)
    axes[1].set_title('Margem Mensal (%)', fontweight='bold'); axes[1].legend()
    plt.tight_layout(); st.pyplot(fig); plt.close()

    st.divider()

    # Regiões
    st.subheader("Performance por Região")
    reg = df.groupby('regiao').agg(receita=('receita','sum'), lucro=('lucro','sum')).reset_index()
    reg['margem'] = reg['lucro']/reg['receita']*100
    reg['share']  = reg['receita']/reg['receita'].sum()*100
    reg = reg.sort_values('receita', ascending=False)

    cc, cd = st.columns(2)
    with cc:
        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.bar(reg['regiao'], reg['receita']/1e6,
                      color=sns.color_palette('Blues_d',len(reg))[::-1], edgecolor='white')
        for bar, row in zip(bars, reg.itertuples()):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.02,
                    f'R$ {row.receita/1e6:.1f}M\n({row.share:.0f}%)',
                    ha='center', fontsize=9, fontweight='bold')
        ax.set_title('Receita por Região (R$ mi)', fontweight='bold')
        plt.tight_layout(); st.pyplot(fig); plt.close()

    with cd:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax2 = ax.twinx()
        ax.bar(reg['regiao'], reg['lucro']/1e6,
               color=sns.color_palette('Greens_d',len(reg))[::-1], alpha=0.85, edgecolor='white')
        ax2.plot(reg['regiao'], reg['margem'], 'ro-', linewidth=2.5, markersize=10)
        for i,(r,m) in enumerate(zip(reg['regiao'], reg['margem'])):
            ax2.text(i, m+0.5, f'{m:.1f}%', ha='center', fontsize=9, color='red', fontweight='bold')
        ax.set_title('Lucro e Margem por Região', fontweight='bold')
        ax.set_ylabel('Lucro (R$ mi)'); ax2.set_ylabel('Margem (%)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.tight_layout(); st.pyplot(fig); plt.close()

    with st.expander("Ver dados brutos"):
        st.dataframe(df.sort_values('receita', ascending=False).reset_index(drop=True),
                     use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PÁGINA 2 — ANÁLISE POR PRODUTO
# ═════════════════════════════════════════════════════════════════════════════
else:
    st.sidebar.subheader("Selecione o Produto")
    produto_sel = st.sidebar.selectbox(
        "Produto", sorted(df_full['produto'].unique()), index=1)

    df_prod = df_full[df_full['produto'] == produto_sel]

    receita_prod  = df_prod['receita'].sum()
    lucro_prod    = df_prod['lucro'].sum()
    margem_prod   = lucro_prod / receita_prod * 100
    qtd_prod      = df_prod['quantidade'].sum()
    ticket_prod   = receita_prod / len(df_prod)

    # Rank de receita
    rank = df_full.groupby('produto')['receita'].sum().rank(ascending=False).astype(int)
    rank_prod = int(rank[produto_sel])
    total_prod = df_full['produto'].nunique()

    # Share de receita
    share = receita_prod / df_full['receita'].sum() * 100

    # Margem relativa à média geral
    margem_media_geral = (df_full['lucro'].sum() / df_full['receita'].sum()) * 100
    delta_margem = margem_prod - margem_media_geral

    st.title(f"📦 Análise: {produto_sel}")
    st.caption(f"Categoria: **{df_prod['categoria'].iloc[0]}**  |  "
               f"Ranking de receita: **{rank_prod}° de {total_prod}**  |  "
               f"Share de mercado: **{share:.1f}%** da receita total")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Receita Total",   f"R$ {receita_prod:,.0f}")
    c2.metric("Lucro Total",     f"R$ {lucro_prod:,.0f}")
    c3.metric("Margem",          f"{margem_prod:.1f}%",
              delta=f"{delta_margem:+.1f}% vs média geral")
    c4.metric("Unidades Vendidas", f"{int(qtd_prod):,}")
    c5.metric("Ticket Médio",    f"R$ {ticket_prod:,.0f}")

    st.divider()

    col1, col2 = st.columns(2)

    # Evolução mensal do produto
    with col1:
        st.subheader("Evolução Mensal")
        men = df_prod.groupby('mes').agg(receita=('receita','sum'), lucro=('lucro','sum')).reset_index()
        men['mes_nome'] = men['mes'].map(nomes_mes)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(men['mes_nome'], men['receita']/1e3, marker='o', color='steelblue',
                linewidth=2.5, markersize=9, label='Receita')
        ax.plot(men['mes_nome'], men['lucro']/1e3, marker='s', color='seagreen',
                linewidth=2.5, markersize=8, label='Lucro')
        ax.fill_between(range(len(men)), men['receita']/1e3, men['lucro']/1e3,
                        alpha=0.1, color='steelblue', label='Custo')
        ax.set_title(f'Receita e Lucro Mensal — {produto_sel}', fontweight='bold')
        ax.set_ylabel('Valor (R$ mil)'); ax.legend()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f'R$ {v:.0f}k'))
        plt.xticks(rotation=30, ha='right'); plt.tight_layout()
        st.pyplot(fig); plt.close()

    # Vendas por região
    with col2:
        st.subheader("Receita por Região")
        reg_p = df_prod.groupby('regiao').agg(receita=('receita','sum')).reset_index()
        reg_p['share'] = reg_p['receita']/reg_p['receita'].sum()*100
        reg_p = reg_p.sort_values('receita', ascending=False)

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(reg_p['regiao'], reg_p['receita']/1e3,
                      color=sns.color_palette('Blues_d', len(reg_p))[::-1], edgecolor='white')
        for bar, row in zip(bars, reg_p.itertuples()):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                    f'{row.share:.0f}%', ha='center', fontsize=10, fontweight='bold')
        ax.set_title(f'Receita por Região — {produto_sel}', fontweight='bold')
        ax.set_ylabel('Receita (R$ mil)')
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f'R$ {v:.0f}k'))
        plt.tight_layout(); st.pyplot(fig); plt.close()

    st.divider()

    # Insights automáticos
    st.subheader("Insights Automáticos")

    melhor_mes  = men.loc[men['receita'].idxmax()]
    pior_mes    = men.loc[men['receita'].idxmin()]
    melhor_reg  = reg_p.iloc[0]
    pior_reg    = reg_p.iloc[-1]

    sinal_margem = "acima" if delta_margem >= 0 else "abaixo"
    emoji_margem = "✅" if delta_margem >= 0 else "⚠️"

    st.info(
        f"**{produto_sel}** gerou **R$ {receita_prod:,.0f}** em 2024, "
        f"ocupando a **{rank_prod}ª posição** em receita entre {total_prod} produtos."
    )

    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.success(f"**Melhor mês:** {melhor_mes['mes_nome']} "
                   f"(R$ {melhor_mes['receita']/1e3:.1f}k)")
        st.success(f"**Melhor região:** {melhor_reg['regiao']} "
                   f"({melhor_reg['share']:.0f}% da receita do produto)")
    with col_i2:
        st.warning(f"**Mês mais fraco:** {pior_mes['mes_nome']} "
                   f"(R$ {pior_mes['receita']/1e3:.1f}k)")
        st.write(f"{emoji_margem} **Margem {sinal_margem} da média geral** em "
                 f"{abs(delta_margem):.1f} pontos percentuais "
                 f"({margem_prod:.1f}% vs {margem_media_geral:.1f}%)")
