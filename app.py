import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Octolab · Sales Dashboard",
    layout="wide",
    page_icon="🔮",
    initial_sidebar_state="expanded",
)

# ── Logo ──────────────────────────────────────────────────────────────────────
LOGO = """<svg width="180" height="44" viewBox="0 0 180 44" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#7c3aed"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
  </defs>
  <rect x="0" y="2" width="40" height="40" rx="10" fill="url(#g1)"/>
  <circle cx="14" cy="15" r="2.5" fill="white"/>
  <circle cx="26" cy="15" r="2.5" fill="white"/>
  <circle cx="20" cy="30" r="2.5" fill="white"/>
  <circle cx="20" cy="9"  r="2.5" fill="white"/>
  <line x1="20" y1="9"  x2="14" y2="15" stroke="white" stroke-width="1.3" opacity="0.85"/>
  <line x1="20" y1="9"  x2="26" y2="15" stroke="white" stroke-width="1.3" opacity="0.85"/>
  <line x1="14" y1="15" x2="20" y2="30" stroke="white" stroke-width="1.3" opacity="0.85"/>
  <line x1="26" y1="15" x2="20" y2="30" stroke="white" stroke-width="1.3" opacity="0.85"/>
  <line x1="14" y1="15" x2="26" y2="15" stroke="white" stroke-width="1.3" opacity="0.85"/>
  <text x="52" y="30" font-family="system-ui,-apple-system,sans-serif" font-weight="800" font-size="22" fill="white">octo</text>
  <text x="108" y="30" font-family="system-ui,-apple-system,sans-serif" font-weight="800" font-size="22" fill="#7c3aed">lab</text>
</svg>"""

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif !important; }

.stApp { background: #09090f; }

header[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"]       { display: none !important; }
#MainMenu                       { display: none !important; }

[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid rgba(124,58,237,0.15) !important;
}

.block-container { padding-top: 1.5rem !important; }

h1, h2, h3 { color: #f8fafc !important; }

hr { border-color: rgba(124,58,237,0.15) !important; }

[data-baseweb="select"] > div {
    background: #1a1a2e !important;
    border-color: rgba(124,58,237,0.25) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
}
[data-baseweb="tag"] { background: rgba(124,58,237,0.2) !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0f0f1a; }
::-webkit-scrollbar-thumb { background: #7c3aed; border-radius: 10px; }

.kpi-card {
    background: linear-gradient(145deg, #141428, #1a1a2e);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 18px;
    padding: 22px 20px 18px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    height: 130px;
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
}
.kpi-label {
    font-size: 11px;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
}
.kpi-value {
    font-size: 26px;
    font-weight: 800;
    color: #f1f5f9;
    line-height: 1;
    margin-bottom: 10px;
}
.kpi-icon {
    position: absolute;
    top: 18px; right: 18px;
    font-size: 26px;
    opacity: 0.12;
}
.kpi-up   { font-size:11px;font-weight:600;color:#10b981;background:rgba(16,185,129,0.1);padding:2px 9px;border-radius:20px;display:inline-block; }
.kpi-down { font-size:11px;font-weight:600;color:#ef4444;background:rgba(239,68,68,0.1);padding:2px 9px;border-radius:20px;display:inline-block; }
.kpi-neu  { font-size:11px;font-weight:600;color:#94a3b8;background:rgba(148,163,184,0.1);padding:2px 9px;border-radius:20px;display:inline-block; }

.section-label {
    font-size: 11px;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
    margin-top: 6px;
}

.badge-live {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(16,185,129,0.1);
    color: #10b981;
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
}

.footer {
    text-align: center;
    padding: 24px;
    color: #334155;
    font-size: 12px;
    border-top: 1px solid rgba(124,58,237,0.1);
    margin-top: 32px;
}
.footer a { color: #7c3aed; text-decoration: none; }
.footer a:hover { text-decoration: underline; }

.chart-card {
    background: #111120;
    border: 1px solid rgba(124,58,237,0.12);
    border-radius: 16px;
    padding: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── Dados ─────────────────────────────────────────────────────────────────────
@st.cache_data
def gerar_dados():
    vendedores = ["Ana Paula", "Carlos Lima", "Fernanda Souza", "Ricardo Alves", "Juliana Costa"]
    produtos   = ["Plano Starter", "Plano Pro", "Plano Enterprise", "Consultoria", "Suporte Premium"]
    status_op  = ["Fechado", "Fechado", "Fechado", "Em negociação", "Perdido"]
    random.seed(42)
    hoje = datetime.today()
    return pd.DataFrame([{
        "data":     hoje - timedelta(days=random.randint(0, 89)),
        "vendedor": random.choice(vendedores),
        "produto":  random.choice(produtos),
        "valor":    random.randint(800, 18000),
        "status":   random.choice(status_op),
    } for _ in range(300)])

df = gerar_dados()
df_fechado = df[df["status"] == "Fechado"].copy()

# ── Helpers ───────────────────────────────────────────────────────────────────
def brl(v):
    return "R$ " + f"{v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

def delta_html(atual, ant):
    if ant == 0: return '<span class="kpi-neu">— sem histórico</span>'
    pct = (atual - ant) / ant * 100
    if pct > 0:  return f'<span class="kpi-up">▲ {pct:.1f}% vs anterior</span>'
    if pct < 0:  return f'<span class="kpi-down">▼ {abs(pct):.1f}% vs anterior</span>'
    return '<span class="kpi-neu">= sem variação</span>'

PURPLE = "#7c3aed"
CYAN   = "#06b6d4"
BG     = "#0d0d1c"
COLORS = [PURPLE, CYAN, "#f59e0b", "#10b981", "#f43f5e"]

def plot_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(color="#e2e8f0", size=14, family="Inter"), x=0.01, pad=dict(l=8)),
        plot_bgcolor=BG, paper_bgcolor=BG,
        font=dict(color="#64748b", family="Inter", size=11),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.04)", tickfont=dict(size=11)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.04)", tickfont=dict(size=11)),
        margin=dict(l=12, r=12, t=48, b=12),
        showlegend=False,
    )

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(LOGO, unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<span class="badge-live">● ao vivo</span>', unsafe_allow_html=True)
    st.markdown("---")

    periodo = st.selectbox("Período", ["Últimos 30 dias", "Últimos 60 dias", "Últimos 90 dias"])
    dias = {"Últimos 30 dias": 30, "Últimos 60 dias": 60, "Últimos 90 dias": 90}[periodo]

    vendedor_filtro = st.multiselect(
        "Vendedores",
        options=sorted(df["vendedor"].unique()),
        default=sorted(df["vendedor"].unique()),
    )

    st.markdown("---")
    st.markdown(f"""
        <p style="color:#475569;font-size:11px;line-height:1.6">
            Atualizado em<br>
            <strong style="color:#94a3b8">{datetime.today().strftime('%d/%m/%Y %H:%M')}</strong>
        </p>
        <p style="color:#334155;font-size:11px;margin-top:12px">
            🔌 Conecte sua base de dados,<br>CRM ou ERP para dados reais.
        </p>
    """, unsafe_allow_html=True)

# ── Filtros ───────────────────────────────────────────────────────────────────
if not vendedor_filtro:
    vendedor_filtro = sorted(df["vendedor"].unique())

corte     = datetime.today() - timedelta(days=dias)
corte_ant = corte - timedelta(days=dias)

df_at = df_fechado[(df_fechado["data"] >= corte) & (df_fechado["vendedor"].isin(vendedor_filtro))]
df_an = df_fechado[(df_fechado["data"] >= corte_ant) & (df_fechado["data"] < corte) & (df_fechado["vendedor"].isin(vendedor_filtro))]

# ── Header ────────────────────────────────────────────────────────────────────
c_title, c_period = st.columns([4, 1])
with c_title:
    st.markdown("""
    <h1 style="font-size:26px;font-weight:800;color:#f1f5f9;margin:0;padding:0;line-height:1.2">
        Sales Dashboard
        <span style="font-size:13px;font-weight:400;color:#475569;margin-left:12px">visão geral de vendas</span>
    </h1>
    """, unsafe_allow_html=True)
with c_period:
    st.markdown(f'<p style="text-align:right;color:#475569;font-size:12px;padding-top:6px">{periodo}</p>', unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
total  = df_at["valor"].sum()
qtd    = len(df_at)
ticket = df_at["valor"].mean() if qtd > 0 else 0
ativos = df_at["vendedor"].nunique()
total_an  = df_an["valor"].sum()
qtd_an    = len(df_an)
ticket_an = df_an["valor"].mean() if qtd_an > 0 else 0

k1, k2, k3, k4 = st.columns(4)
for col, icon, label, val, ant in [
    (k1, "💰", "Receita Total",      brl(total),  delta_html(total, total_an)),
    (k2, "🤝", "Deals Fechados",     str(qtd),    delta_html(qtd, qtd_an)),
    (k3, "🎯", "Ticket Médio",       brl(ticket), delta_html(ticket, ticket_an)),
    (k4, "👥", "Vendedores Ativos",  str(ativos), ""),
]:
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{val}</div>
        {ant}
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ── Gráficos linha 1 ──────────────────────────────────────────────────────────
g1, g2 = st.columns([3, 2])

with g1:
    rank = df_at.groupby("vendedor")["valor"].sum().reset_index().sort_values("valor", ascending=True)
    fig = go.Figure(go.Bar(
        x=rank["valor"], y=rank["vendedor"],
        orientation="h",
        marker=dict(
            color=rank["valor"],
            colorscale=[[0, "#3b0764"], [0.5, PURPLE], [1, CYAN]],
            line=dict(width=0),
        ),
        text=[brl(v) for v in rank["valor"]],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=11),
        hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>",
    ))
    l = plot_layout("Receita por Vendedor")
    l["xaxis"].update(showgrid=False, showticklabels=False)
    l["yaxis"].update(tickfont=dict(color="#94a3b8", size=12))
    fig.update_layout(**l)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with g2:
    por_prod = df_at.groupby("produto")["valor"].sum().reset_index()
    fig2 = go.Figure(go.Pie(
        labels=por_prod["produto"],
        values=por_prod["valor"],
        hole=0.6,
        marker=dict(colors=COLORS, line=dict(color=BG, width=2)),
        textinfo="percent",
        textfont=dict(size=11, color="#e2e8f0"),
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
    ))
    l2 = plot_layout("Mix de Produtos")
    l2.pop("xaxis", None); l2.pop("yaxis", None)
    l2.update(showlegend=True, legend=dict(
        font=dict(size=10, color="#64748b"),
        bgcolor="rgba(0,0,0,0)",
        orientation="v", x=1.02, y=0.5,
    ))
    fig2.update_layout(**l2)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ── Evolução semanal ──────────────────────────────────────────────────────────
df_ev = df_at.copy()
df_ev["semana"] = df_ev["data"].dt.to_period("W").dt.start_time
evo = df_ev.groupby("semana")["valor"].sum().reset_index()

fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=evo["semana"], y=evo["valor"],
    mode="lines+markers",
    line=dict(color=PURPLE, width=2.5, shape="spline"),
    marker=dict(size=7, color=PURPLE, line=dict(color=CYAN, width=2)),
    fill="tozeroy",
    fillcolor="rgba(124,58,237,0.07)",
    hovertemplate="<b>Semana %{x|%d/%m/%Y}</b><br>Receita: %{y:,.0f}<extra></extra>",
))
l3 = plot_layout("Evolução Semanal de Receita")
l3["yaxis"].update(tickprefix="R$ ", tickformat=",.0f")
l3["margin"]["b"] = 24
fig3.update_layout(**l3)
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

# ── Funil + Tabela ────────────────────────────────────────────────────────────
g3, g4 = st.columns([1, 2])

with g3:
    df_full = df[(df["vendedor"].isin(vendedor_filtro)) & (df["data"] >= corte)]
    funil = df_full.groupby("status").size().reset_index(name="qtd").sort_values("qtd", ascending=False)
    status_order = ["Fechado", "Em negociação", "Perdido"]
    funil["ordem"] = funil["status"].map({s: i for i, s in enumerate(status_order)})
    funil = funil.sort_values("ordem")

    fig4 = go.Figure(go.Funnel(
        y=funil["status"], x=funil["qtd"],
        textinfo="value+percent initial",
        textfont=dict(color="#e2e8f0", size=12),
        marker=dict(color=[PURPLE, CYAN, "#334155"], line=dict(color=BG, width=1)),
        connector=dict(line=dict(color=BG, width=1)),
    ))
    l4 = plot_layout("Funil de Negócios")
    l4.pop("xaxis", None); l4.pop("yaxis", None)
    fig4.update_layout(**l4)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

with g4:
    st.markdown('<div class="section-label">Últimas vendas fechadas</div>', unsafe_allow_html=True)
    tabela = df_at.sort_values("data", ascending=False).head(10).copy()
    tabela["data"]  = tabela["data"].dt.strftime("%d/%m/%Y")
    tabela["valor"] = tabela["valor"].apply(brl)
    st.dataframe(
        tabela[["data","vendedor","produto","valor"]].rename(columns={
            "data": "Data", "vendedor": "Vendedor",
            "produto": "Produto", "valor": "Valor"
        }),
        use_container_width=True,
        hide_index=True,
        height=300,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    💡 Este dashboard pode ser conectado ao seu banco de dados, CRM ou ERP &nbsp;·&nbsp;
    Feito por <a href="https://github.com/fabiicarniel" target="_blank">Octolab</a>
    &nbsp;·&nbsp; <a href="https://github.com/fabiicarniel/octolab-sales-dashboard" target="_blank">Ver código no GitHub</a>
</div>
""", unsafe_allow_html=True)
