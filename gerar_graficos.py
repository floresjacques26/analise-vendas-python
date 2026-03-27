"""Script auxiliar: gera o dataset e salva os gráficos em assets/"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

np.random.seed(42)
Path("assets").mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="husl")
plt.rcParams['font.size'] = 12

# ── Dataset ──────────────────────────────────────────────────────────────────
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
df.to_csv('data/vendas.csv', index=False)
print(f"Dataset: {df.shape}")

# ── Gráfico 1 — Produtos ─────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
receita_prod = df.groupby('produto')['receita'].sum().sort_values()
receita_prod.plot(kind='barh', ax=axes[0], color=sns.color_palette('Blues', len(receita_prod)))
axes[0].set_title('Receita Total por Produto', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Receita (R$)')
axes[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'R$ {x/1e6:.1f}M'))
for i, v in enumerate(receita_prod.values):
    axes[0].text(v+5000, i, f'R$ {v/1e6:.2f}M', va='center', fontsize=9)

qtd_prod = df.groupby('produto')['quantidade'].sum().sort_values()
qtd_prod.plot(kind='barh', ax=axes[1], color=sns.color_palette('Greens', len(qtd_prod)))
axes[1].set_title('Quantidade Vendida por Produto', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Unidades')
axes[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'{int(x):,}'))
for i, v in enumerate(qtd_prod.values):
    axes[1].text(v+20, i, f'{int(v):,}', va='center', fontsize=9)

plt.suptitle('Análise de Produtos', fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('assets/grafico_produtos.png', dpi=150, bbox_inches='tight')
plt.close()
print("OK grafico_produtos.png")

# ── Gráfico 2 — Mensal ───────────────────────────────────────────────────────
nomes_mes = {1:'Jan',2:'Fev',3:'Mar',4:'Abr',5:'Mai',6:'Jun',
             7:'Jul',8:'Ago',9:'Set',10:'Out',11:'Nov',12:'Dez'}
mensal = df.groupby('mes').agg(receita=('receita','sum'), lucro=('lucro','sum')).reset_index()
mensal['mes_nome'] = mensal['mes'].map(nomes_mes)
mensal['margem']   = mensal['lucro'] / mensal['receita'] * 100

fig, axes = plt.subplots(2, 1, figsize=(14, 10))
x, w = np.arange(len(mensal)), 0.38
axes[0].bar(x-w/2, mensal['receita']/1e3, w, label='Receita', color='steelblue', alpha=0.85)
axes[0].bar(x+w/2, mensal['lucro']/1e3,   w, label='Lucro',   color='seagreen',  alpha=0.85)
axes[0].set_xticks(x); axes[0].set_xticklabels(mensal['mes_nome'])
axes[0].set_title('Receita e Lucro Mensal (R$ mil)', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Valor (R$ mil)'); axes[0].legend()
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f'R$ {v:.0f}k'))

axes[1].plot(mensal['mes_nome'], mensal['margem'], marker='o', linewidth=2.5,
             color='darkorange', markersize=9)
axes[1].fill_between(range(len(mensal)), mensal['margem'], alpha=0.15, color='darkorange')
axes[1].axhline(mensal['margem'].mean(), color='navy', linestyle='--', linewidth=1.5,
                label=f'Média: {mensal["margem"].mean():.1f}%')
for i, m in enumerate(mensal['margem']):
    axes[1].text(i, m+0.3, f'{m:.1f}%', ha='center', fontsize=9)
axes[1].set_title('Margem de Lucro Mensal (%)', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Margem (%)'); axes[1].legend()

plt.tight_layout()
plt.savefig('assets/grafico_mensal.png', dpi=150, bbox_inches='tight')
plt.close()
print("OK grafico_mensal.png")

# ── Gráfico 3 — Regiões ──────────────────────────────────────────────────────
reg = df.groupby('regiao').agg(receita=('receita','sum'), lucro=('lucro','sum')).reset_index()
reg['margem'] = reg['lucro']/reg['receita']*100
reg['share']  = reg['receita']/reg['receita'].sum()*100
reg = reg.sort_values('receita', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
bars = axes[0].bar(reg['regiao'], reg['receita']/1e6,
                   color=sns.color_palette('Blues_d',len(reg))[::-1], edgecolor='white')
axes[0].set_title('Receita por Região (R$ milhões)', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Receita (R$ mi)')
for bar, row in zip(bars, reg.itertuples()):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.02,
                 f'R$ {row.receita/1e6:.1f}M\n({row.share:.0f}%)',
                 ha='center', fontsize=10, fontweight='bold')

ax2 = axes[1].twinx()
axes[1].bar(reg['regiao'], reg['lucro']/1e6,
            color=sns.color_palette('Greens_d',len(reg))[::-1], alpha=0.85, edgecolor='white')
ax2.plot(reg['regiao'], reg['margem'], 'ro-', linewidth=2.5, markersize=10, label='Margem %')
for i,(r,m) in enumerate(zip(reg['regiao'], reg['margem'])):
    ax2.text(i, m+0.4, f'{m:.1f}%', ha='center', fontsize=9, color='red', fontweight='bold')
axes[1].set_title('Lucro por Região e Margem (%)', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Lucro (R$ mi)'); ax2.set_ylabel('Margem (%)', color='red')
ax2.tick_params(axis='y', labelcolor='red'); ax2.legend(loc='upper right')

plt.tight_layout()
plt.savefig('assets/grafico_regioes.png', dpi=150, bbox_inches='tight')
plt.close()
print("OK grafico_regioes.png")

# ── Gráfico 4 — Margem por produto ───────────────────────────────────────────
margem_prod = df.groupby('produto').agg(receita=('receita','sum'), lucro=('lucro','sum'))
margem_prod['margem'] = margem_prod['lucro']/margem_prod['receita']*100
margem_prod = margem_prod.sort_values('margem', ascending=False)
media = margem_prod['margem'].mean()
colors = ['seagreen' if m >= media else 'tomato' for m in margem_prod['margem']]

fig, ax = plt.subplots(figsize=(13, 6))
bars = ax.bar(margem_prod.index, margem_prod['margem'], color=colors, edgecolor='white')
ax.axhline(media, color='navy', linestyle='--', linewidth=2, label=f'Média: {media:.1f}%')
for bar, val in zip(bars, margem_prod['margem']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
            f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')
ax.set_title('Margem de Lucro por Produto', fontsize=14, fontweight='bold')
ax.set_ylabel('Margem (%)'); ax.legend()
plt.xticks(rotation=30, ha='right'); plt.tight_layout()
plt.savefig('assets/grafico_margem.png', dpi=150, bbox_inches='tight')
plt.close()
print("OK grafico_margem.png")

print("\nGraficos gerados em assets/")
print(f"\nMetricas:")
print(f"  Receita total : R$ {df['receita'].sum():,.2f}")
print(f"  Lucro total   : R$ {df['lucro'].sum():,.2f}")
print(f"  Margem geral  : {df['lucro'].sum()/df['receita'].sum()*100:.1f}%")
