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

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Análise de Vendas 2024",
    page_icon="📊",
    layout="wide",
)

sns.set_theme(style="whitegrid")

# ── Geração / carregamento dos dados ─────────────────────────────────────────
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

        prod_col   = np.random.choice(produtos, N, p=pesos_prod)
        mes_col    = np.random.choice(range(1,13), N, p=pesos_mes)
        dia_col    = np.random.randint(1, 28, N)
        regiao_col = np.random.choice(regioes, N, p=pesos_regiao)
        qtd_col    = np.random.randint(1, 8, N)

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

# ── Sidebar — filtros ─────────────────────────────────────────────────────────
st.sidebar.title("Filtros")

regioes_disp = sorted(df_full['regiao'].unique())
regioes_sel  = st.sidebar.multiselect("Região", regioes_disp, default=regioes_disp)

categorias_disp = sorted(df_full['categoria'].unique())
cats_sel        = st.sidebar.multiselect("Categoria", categorias_disp, default=categorias_disp)

meses_disp = list(range(1, 13))
nomes_mes  = {1:'Jan',2:'Fev',3:'Mar',4:'Abr',5:'Mai',6:'Jun',
              7:'Jul',8:'Ago',9:'Set',10:'Out',11:'Nov',12:'Dez'}
mes_range  = st.sidebar.select_slider(
    "Período (mês)",
    options=meses_disp,
    value=(1, 12),
    format_func=lambda m: nomes_mes[m],
)

df = df_full[
    df_full['regiao'].isin(regioes_sel) &
    df_full['categoria'].isin(cats_sel) &
    df_full['mes'].between(mes_range[0], mes_range[1])
].copy()

# ── Título ────────────────────────────────────────────────────────────────────
st.title("📊 Análise de Vendas — Eletrônicos Brasil 2024")
st.caption(f"Exibindo {len(df):,} de {len(df_full):,} transações com os filtros selecionados.")

# ── KPIs ──────────────────────────────────────────────────────────────────────
receita = df['receita'].sum()
lucro   = df['lucro'].sum()
margem  = lucro / receita * 100 if receita > 0 else 0
ticket  = receita / len(df) if len(df) > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Receita Total",   f"R$ {receita:,.0f}")
col2.metric("Lucro Total",     f"R$ {lucro:,.0f}")
col3.metric("Margem Média",    f"{margem:.1f}%")
col4.metric("Ticket Médio",    f"R$ {ticket:,.0f}")

st.divider()

# ── Linha 1: Produtos ─────────────────────────────────────────────────────────
st.subheader("Análise por Produto")
col_a, col_b = st.columns(2)

with col_a:
    fig, ax = plt.subplots(figsize=(8, 5))
    rp = df.groupby('produto')['receita'].sum().sort_values()
    rp.plot(kind='barh', ax=ax, color=sns.color_palette('Blues', len(rp)))
    ax.set_title('Receita por Produto', fontweight='bold')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'R$ {x/1e6:.1f}M'))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_b:
    fig, ax = plt.subplots(figsize=(8, 5))
    mp = df.groupby('produto').apply(lambda x: x['lucro'].sum()/x['receita'].sum()*100).sort_values(ascending=False)
    media_m = mp.mean()
    colors  = ['seagreen' if v >= media_m else 'tomato' for v in mp]
    mp.plot(kind='bar', ax=ax, color=colors, edgecolor='white')
    ax.axhline(media_m, color='navy', linestyle='--', linewidth=1.5, label=f'Média: {media_m:.1f}%')
    ax.set_title('Margem de Lucro por Produto', fontweight='bold')
    ax.set_ylabel('Margem (%)')
    ax.legend(); plt.xticks(rotation=30, ha='right'); plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.divider()

# ── Linha 2: Mensal ───────────────────────────────────────────────────────────
st.subheader("Sazonalidade Mensal")

mensal = df.groupby('mes').agg(receita=('receita','sum'), lucro=('lucro','sum')).reset_index()
mensal['mes_nome'] = mensal['mes'].map(nomes_mes)
mensal['margem']   = mensal['lucro'] / mensal['receita'] * 100

fig, axes = plt.subplots(1, 2, figsize=(16, 5))
x, w = np.arange(len(mensal)), 0.38
axes[0].bar(x-w/2, mensal['receita']/1e3, w, label='Receita', color='steelblue', alpha=0.85)
axes[0].bar(x+w/2, mensal['lucro']/1e3,   w, label='Lucro',   color='seagreen',  alpha=0.85)
axes[0].set_xticks(x); axes[0].set_xticklabels(mensal['mes_nome'])
axes[0].set_title('Receita e Lucro Mensal (R$ mil)', fontweight='bold')
axes[0].legend()
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f'R$ {v:.0f}k'))

axes[1].plot(mensal['mes_nome'], mensal['margem'], marker='o', color='darkorange', linewidth=2.5, markersize=8)
axes[1].fill_between(range(len(mensal)), mensal['margem'], alpha=0.15, color='darkorange')
axes[1].axhline(mensal['margem'].mean(), color='navy', linestyle='--', linewidth=1.5,
                label=f'Média: {mensal["margem"].mean():.1f}%')
axes[1].set_title('Margem Mensal (%)', fontweight='bold')
axes[1].set_ylabel('Margem (%)'); axes[1].legend()
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.divider()

# ── Linha 3: Regiões ──────────────────────────────────────────────────────────
st.subheader("Performance por Região")

reg = df.groupby('regiao').agg(receita=('receita','sum'), lucro=('lucro','sum')).reset_index()
reg['margem'] = reg['lucro']/reg['receita']*100
reg['share']  = reg['receita']/reg['receita'].sum()*100
reg = reg.sort_values('receita', ascending=False)

col_c, col_d = st.columns(2)
with col_c:
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(reg['regiao'], reg['receita']/1e6,
                  color=sns.color_palette('Blues_d',len(reg))[::-1], edgecolor='white')
    for bar, row in zip(bars, reg.itertuples()):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.02,
                f'R$ {row.receita/1e6:.1f}M\n({row.share:.0f}%)',
                ha='center', fontsize=9, fontweight='bold')
    ax.set_title('Receita por Região (R$ milhões)', fontweight='bold')
    plt.tight_layout(); st.pyplot(fig); plt.close()

with col_d:
    fig, ax = plt.subplots(figsize=(7, 5))
    ax2 = ax.twinx()
    ax.bar(reg['regiao'], reg['lucro']/1e6,
           color=sns.color_palette('Greens_d',len(reg))[::-1], alpha=0.85, edgecolor='white')
    ax2.plot(reg['regiao'], reg['margem'], 'ro-', linewidth=2.5, markersize=10)
    for i,(r,m) in enumerate(zip(reg['regiao'], reg['margem'])):
        ax2.text(i, m+0.4, f'{m:.1f}%', ha='center', fontsize=9, color='red', fontweight='bold')
    ax.set_title('Lucro e Margem por Região', fontweight='bold')
    ax.set_ylabel('Lucro (R$ mi)'); ax2.set_ylabel('Margem (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    plt.tight_layout(); st.pyplot(fig); plt.close()

st.divider()

# ── Tabela de dados ───────────────────────────────────────────────────────────
with st.expander("Ver dados brutos"):
    st.dataframe(
        df.sort_values('receita', ascending=False).reset_index(drop=True),
        use_container_width=True,
    )
