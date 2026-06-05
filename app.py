import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Octolab · Sales Dashboard",
    layout="wide",
    page_icon="🔮",
    initial_sidebar_state="expanded",
)

LOGO = """<svg width="180" height="44" viewBox="0 0 180 44" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
  </defs>
  <rect x="0" y="2" width="40" height="40" rx="10" fill="url(#g1)"/>
  <circle cx="14" cy="15" r="2.5" fill="white"/><circle cx="26" cy="15" r="2.5" fill="white"/>
  <circle cx="20" cy="30" r="2.5" fill="white"/><circle cx="20" cy="9" r="2.5" fill="white"/>
  <line x1="20" y1="9" x2="14" y2="15" stroke="white" stroke-width="1.3" opacity="0.85"/>
  <line x1="20" y1="9" x2="26" y2="15" stroke="white" stroke-width="1.3" opacity="0.85"/>
  <line x1="14" y1="15" x2="20" y2="30" stroke="white" stroke-width="1.3" opacity="0.85"/>
  <line x1="26" y1="15" x2="20" y2="30" stroke="white" stroke-width="1.3" opacity="0.85"/>
  <line x1="14" y1="15" x2="26" y2="15" stroke="white" stroke-width="1.3" opacity="0.85"/>
  <text x="52" y="30" font-family="system-ui,-apple-system,sans-serif" font-weight="800" font-size="22" fill="white">octo</text>
  <text x="108" y="30" font-family="system-ui,-apple-system,sans-serif" font-weight="800" font-size="22" fill="#7c3aed">lab</text>
</svg>"""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"],.stApp{font-family:'Inter',sans-serif !important;}
.stApp{background:#09090f;}
header[data-testid="stHeader"],[data-testid="stToolbar"],#MainMenu{display:none !important;}
[data-testid="stSidebar"]{background:#0f0f1a !important;border-right:1px solid rgba(124,58,237,0.15) !important;}
.block-container{padding-top:1.5rem !important;}
h1,h2,h3{color:#f8fafc !important;}
hr{border-color:rgba(124,58,237,0.15) !important;}
[data-baseweb="select"]>div{background:#1a1a2e !important;border-color:rgba(124,58,237,0.25) !important;border-radius:10px !important;color:#f8fafc !important;}
[data-baseweb="tag"]{background:rgba(124,58,237,0.2) !important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:#0f0f1a;}
::-webkit-scrollbar-thumb{background:#7c3aed;border-radius:10px;}
/* Tabs */
[data-testid="stTabs"] button{color:#64748b !important;font-weight:500 !important;font-size:13px !important;border-radius:0 !important;}
[data-testid="stTabs"] button[aria-selected="true"]{color:#f1f5f9 !important;border-bottom:2px solid #7c3aed !important;}
[data-testid="stTabs"] button:hover{color:#c4b5fd !important;}
/* KPI cards */
.kpi-card{background:linear-gradient(145deg,#141428,#1a1a2e);border:1px solid rgba(124,58,237,0.2);border-radius:18px;padding:22px 20px 18px;position:relative;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.4);height:130px;}
.kpi-card::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#7c3aed,#06b6d4);}
.kpi-card-meta::after{background:linear-gradient(90deg,#f59e0b,#ef4444);}
.kpi-label{font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;}
.kpi-value{font-size:26px;font-weight:800;color:#f1f5f9;line-height:1;margin-bottom:10px;}
.kpi-icon{position:absolute;top:18px;right:18px;font-size:26px;opacity:.12;}
.kpi-up{font-size:11px;font-weight:600;color:#10b981;background:rgba(16,185,129,.1);padding:2px 9px;border-radius:20px;display:inline-block;}
.kpi-down{font-size:11px;font-weight:600;color:#ef4444;background:rgba(239,68,68,.1);padding:2px 9px;border-radius:20px;display:inline-block;}
.kpi-neu{font-size:11px;font-weight:600;color:#94a3b8;background:rgba(148,163,184,.1);padding:2px 9px;border-radius:20px;display:inline-block;}
.meta-bar-bg{background:rgba(255,255,255,0.06);border-radius:99px;height:6px;margin-top:8px;overflow:hidden;}
.meta-bar-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,#f59e0b,#ef4444);}
/* Badges */
.badge-live{display:inline-flex;align-items:center;gap:5px;background:rgba(16,185,129,.1);color:#10b981;border:1px solid rgba(16,185,129,.25);border-radius:20px;padding:3px 10px;font-size:11px;font-weight:600;}
/* Section label */
.section-label{font-size:11px;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;margin-top:6px;}
/* Top deal card */
.top-deal{background:linear-gradient(145deg,#141428,#1a1a2e);border:1px solid rgba(124,58,237,0.2);border-radius:14px;padding:16px;box-shadow:0 4px 16px rgba(0,0,0,.3);}
.top-deal-rank{font-size:22px;margin-bottom:6px;}
.top-deal-val{font-size:20px;font-weight:800;color:#f1f5f9;}
.top-deal-sub{font-size:11px;color:#64748b;margin-top:4px;}
/* Download button */
[data-testid="stDownloadButton"] button{background:rgba(124,58,237,.15) !important;border:1px solid rgba(124,58,237,.3) !important;color:#c4b5fd !important;border-radius:10px !important;font-weight:600 !important;}
[data-testid="stDownloadButton"] button:hover{background:rgba(124,58,237,.25) !important;}
/* Footer */
.footer{text-align:center;padding:24px;color:#334155;font-size:12px;border-top:1px solid rgba(124,58,237,.1);margin-top:32px;}
.footer a{color:#7c3aed;text-decoration:none;}
</style>
""", unsafe_allow_html=True)

# ── Dados ─────────────────────────────────────────────────────────────────────
@st.cache_data
def gerar_dados():
    vendedores = ["Ana Paula", "Carlos Lima", "Fernanda Souza", "Ricardo Alves", "Juliana Costa"]
    produtos   = ["Plano Starter", "Plano Pro", "Plano Enterprise", "Consultoria", "Suporte Premium"]
    canais     = ["Indicação", "LinkedIn", "Site", "Outbound", "Parceiro"]
    status_op  = ["Fechado", "Fechado", "Fechado", "Em negociação", "Perdido"]
    random.seed(42)
    hoje = datetime.today()
    return pd.DataFrame([{
        "data":       hoje - timedelta(days=random.randint(0, 89)),
        "vendedor":   random.choice(vendedores),
        "produto":    random.choice(produtos),
        "canal":      random.choice(canais),
        "valor":      random.randint(800, 18000),
        "status":     random.choice(status_op),
        "dias_ciclo": random.randint(3, 45),
    } for _ in range(400)])

df = gerar_dados()
df_fechado = df[df["status"] == "Fechado"].copy()

# ── Helpers ───────────────────────────────────────────────────────────────────
def brl(v):
    return "R$ " + f"{v:,.0f}".replace(",","X").replace(".",",").replace("X",".")

def delta_html(a, b):
    if b == 0: return '<span class="kpi-neu">— sem histórico</span>'
    p = (a - b) / b * 100
    if p > 0:  return f'<span class="kpi-up">▲ {p:.1f}% vs anterior</span>'
    if p < 0:  return f'<span class="kpi-down">▼ {abs(p):.1f}% vs anterior</span>'
    return '<span class="kpi-neu">= sem variação</span>'

PU, CY, BG = "#7c3aed", "#06b6d4", "#0d0d1c"
COLORS = [PU, CY, "#f59e0b", "#10b981", "#f43f5e"]

def plot_layout(title="", height=340):
    return dict(
        title=dict(text=title, font=dict(color="#e2e8f0", size=14, family="Inter"), x=0.01),
        plot_bgcolor=BG, paper_bgcolor=BG,
        font=dict(color="#64748b", family="Inter", size=11),
        height=height,
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.04)"),
        margin=dict(l=12, r=12, t=44, b=12),
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

    meta_mensal = st.number_input("Meta mensal (R$)", min_value=0, value=250000, step=10000)

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

df_at = df_fechado[(df_fechado["data"] >= corte) & (df_fechado["vendedor"].isin(vendedor_filtro))].copy()
df_an = df_fechado[(df_fechado["data"] >= corte_ant) & (df_fechado["data"] < corte) & (df_fechado["vendedor"].isin(vendedor_filtro))].copy()
df_all = df[(df["data"] >= corte) & (df["vendedor"].isin(vendedor_filtro))].copy()

# ── Header ────────────────────────────────────────────────────────────────────
c_t, c_p = st.columns([4, 1])
with c_t:
    st.markdown('<h1 style="font-size:26px;font-weight:800;color:#f1f5f9;margin:0;line-height:1.2">Sales Dashboard <span style="font-size:13px;font-weight:400;color:#475569;margin-left:10px">visão geral de vendas</span></h1>', unsafe_allow_html=True)
with c_p:
    st.markdown(f'<p style="text-align:right;color:#475569;font-size:12px;padding-top:6px">{periodo}</p>', unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
total  = df_at["valor"].sum()
qtd    = len(df_at)
ticket = df_at["valor"].mean() if qtd > 0 else 0
ciclo  = df_at["dias_ciclo"].mean() if qtd > 0 else 0
total_an  = df_an["valor"].sum()
qtd_an    = len(df_an)
ticket_an = df_an["valor"].mean() if qtd_an > 0 else 0
meta_pct  = min(total / meta_mensal * 100, 100) if meta_mensal > 0 else 0

k1, k2, k3, k4, k5 = st.columns(5)

for col, icon, label, val, delta, extra_cls in [
    (k1, "💰", "Receita Total",    brl(total),         delta_html(total, total_an), ""),
    (k2, "🤝", "Deals Fechados",   str(qtd),           delta_html(qtd, qtd_an),     ""),
    (k3, "🎯", "Ticket Médio",     brl(ticket),        delta_html(ticket, ticket_an),""),
    (k4, "⏱️", "Ciclo Médio",      f"{ciclo:.0f} dias", "",                         ""),
]:
    col.markdown(f"""
    <div class="kpi-card {extra_cls}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{val}</div>
        {delta}
    </div>""", unsafe_allow_html=True)

k5.markdown(f"""
<div class="kpi-card kpi-card-meta">
    <div class="kpi-icon">🏆</div>
    <div class="kpi-label">Meta Mensal</div>
    <div class="kpi-value">{meta_pct:.0f}%</div>
    <div class="meta-bar-bg"><div class="meta-bar-fill" style="width:{meta_pct}%"></div></div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊  Visão Geral", "👥  Vendedores", "📦  Produtos & Canais", "🔍  Detalhes"])

# ════════════════════════════════ TAB 1 ══════════════════════════════════════
with tab1:
    # Evolução semanal + forecast
    df_ev = df_at.copy()
    df_ev["semana"] = df_ev["data"].dt.to_period("W").dt.start_time
    evo = df_ev.groupby("semana")["valor"].sum().reset_index()

    fig_ev = go.Figure()
    fig_ev.add_trace(go.Scatter(
        x=evo["semana"], y=evo["valor"],
        mode="lines+markers", name="Realizado",
        line=dict(color=PU, width=2.5, shape="spline"),
        marker=dict(size=7, color=PU, line=dict(color=CY, width=2)),
        fill="tozeroy", fillcolor="rgba(124,58,237,0.07)",
        hovertemplate="<b>%{x|%d/%m/%Y}</b><br>%{y:,.0f}<extra></extra>",
    ))
    if len(evo) >= 3:
        x_num = np.arange(len(evo))
        z = np.polyfit(x_num, evo["valor"], 1)
        p = np.poly1d(z)
        last_date = evo["semana"].iloc[-1]
        future_dates = [last_date + timedelta(weeks=i) for i in range(1, 4)]
        future_y = [max(0, p(len(evo) + i - 1)) for i in range(1, 4)]
        fig_ev.add_trace(go.Scatter(
            x=[evo["semana"].iloc[-1]] + future_dates,
            y=[evo["valor"].iloc[-1]] + future_y,
            mode="lines", name="Projeção",
            line=dict(color=CY, width=2, dash="dot"),
            hovertemplate="<b>Projeção %{x|%d/%m/%Y}</b><br>%{y:,.0f}<extra></extra>",
        ))
    l_ev = plot_layout("Evolução Semanal de Receita + Projeção", height=300)
    l_ev["showlegend"] = True
    l_ev["legend"] = dict(font=dict(size=11, color="#94a3b8"), bgcolor="rgba(0,0,0,0)", x=0.01, y=0.99)
    l_ev["yaxis"]["tickprefix"] = "R$ "
    l_ev["yaxis"]["tickformat"] = ",.0f"
    fig_ev.update_layout(**l_ev)
    st.plotly_chart(fig_ev, use_container_width=True, config={"displayModeBar": False})

    # Top 3 deals + Dia da semana
    c_top, c_dow = st.columns([1, 2])

    with c_top:
        st.markdown('<div class="section-label">🏆 Top 3 Deals</div>', unsafe_allow_html=True)
        medals = ["🥇", "🥈", "🥉"]
        top3 = df_at.nlargest(3, "valor")
        for i, (_, row) in enumerate(top3.iterrows()):
            st.markdown(f"""
            <div class="top-deal" style="margin-bottom:8px">
                <div class="top-deal-rank">{medals[i]}</div>
                <div class="top-deal-val">{brl(row['valor'])}</div>
                <div class="top-deal-sub">{row['vendedor']} · {row['produto']}</div>
                <div class="top-deal-sub">{row['data'].strftime('%d/%m/%Y')}</div>
            </div>""", unsafe_allow_html=True)

    with c_dow:
        dias_map = {"Monday":"Seg","Tuesday":"Ter","Wednesday":"Qua","Thursday":"Qui","Friday":"Sex","Saturday":"Sáb","Sunday":"Dom"}
        ordem = ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]
        df_at_d = df_at.copy()
        df_at_d["dia"] = df_at_d["data"].dt.day_name().map(dias_map)
        dow = df_at_d.groupby("dia").agg(deals=("valor","count"), receita=("valor","sum")).reindex(ordem).fillna(0).reset_index()
        fig_dow = go.Figure(go.Bar(
            x=dow["dia"], y=dow["receita"],
            marker=dict(color=dow["receita"], colorscale=[[0,"#1e1b4b"],[1,PU]], line=dict(width=0)),
            text=[brl(v) for v in dow["receita"]],
            textposition="outside", textfont=dict(color="#64748b", size=10),
            hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>",
        ))
        l_dow = plot_layout("Receita por Dia da Semana", height=320)
        l_dow["xaxis"]["tickfont"] = dict(color="#94a3b8", size=12)
        l_dow["yaxis"]["showgrid"] = False
        l_dow["yaxis"]["showticklabels"] = False
        fig_dow.update_layout(**l_dow)
        st.plotly_chart(fig_dow, use_container_width=True, config={"displayModeBar": False})

# ════════════════════════════════ TAB 2 ══════════════════════════════════════
with tab2:
    # Performance table
    stats = df_all.groupby("vendedor").agg(
        total=("status","count"),
        fechados=("status", lambda x: (x=="Fechado").sum()),
        ciclo=("dias_ciclo","mean"),
    ).reset_index()
    rec = df_at.groupby("vendedor").agg(receita=("valor","sum"), ticket=("valor","mean")).reset_index()
    stats = stats.merge(rec, on="vendedor", how="left").fillna(0)
    stats["win_rate"] = (stats["fechados"] / stats["total"] * 100).round(1)
    stats["ciclo"] = stats["ciclo"].round(0).astype(int)
    stats["receita"] = stats["receita"].round(0).astype(int)
    stats["ticket"]  = stats["ticket"].round(0).astype(int)
    stats = stats.sort_values("receita", ascending=False)

    st.markdown('<div class="section-label">Performance por Vendedor</div>', unsafe_allow_html=True)
    st.dataframe(
        stats.rename(columns={"vendedor":"Vendedor","total":"Total Ops","fechados":"Fechados",
                               "receita":"Receita (R$)","ticket":"Ticket Médio (R$)",
                               "win_rate":"Win Rate (%)","ciclo":"Ciclo Médio (dias)"}),
        column_config={
            "Win Rate (%)": st.column_config.ProgressColumn("Win Rate", format="%.1f%%", min_value=0, max_value=100),
            "Receita (R$)": st.column_config.NumberColumn("Receita", format="R$ %d"),
            "Ticket Médio (R$)": st.column_config.NumberColumn("Ticket Médio", format="R$ %d"),
        },
        use_container_width=True, hide_index=True, height=240,
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Heatmap vendedor x produto
    c_heat, c_ciclo = st.columns(2)

    with c_heat:
        pivot = df_at.groupby(["vendedor","produto"])["valor"].sum().unstack(fill_value=0)
        fig_h = go.Figure(go.Heatmap(
            z=pivot.values, x=list(pivot.columns), y=list(pivot.index),
            colorscale=[[0,"#0f0f1a"],[0.4,"#3b0764"],[1,CY]],
            text=[[brl(v) for v in row] for row in pivot.values],
            texttemplate="%{text}", textfont=dict(size=10, color="white"),
            hovertemplate="<b>%{y} × %{x}</b><br>%{text}<extra></extra>",
            showscale=False,
        ))
        l_h = plot_layout("Receita: Vendedor × Produto", height=280)
        l_h.pop("xaxis",None); l_h.pop("yaxis",None)
        l_h["xaxis"] = dict(tickfont=dict(color="#94a3b8",size=10),tickangle=-20)
        l_h["yaxis"] = dict(tickfont=dict(color="#94a3b8",size=11))
        fig_h.update_layout(**l_h)
        st.plotly_chart(fig_h, use_container_width=True, config={"displayModeBar": False})

    with c_ciclo:
        ciclo_vend = df_at.groupby("vendedor")["dias_ciclo"].mean().reset_index().sort_values("dias_ciclo")
        fig_c = go.Figure(go.Bar(
            x=ciclo_vend["dias_ciclo"], y=ciclo_vend["vendedor"],
            orientation="h",
            marker=dict(color=ciclo_vend["dias_ciclo"], colorscale=[[0,CY],[1,PU]], line=dict(width=0)),
            text=[f"{v:.0f} dias" for v in ciclo_vend["dias_ciclo"]],
            textposition="outside", textfont=dict(color="#94a3b8", size=11),
            hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>",
        ))
        l_c = plot_layout("Ciclo Médio de Vendas (dias)", height=280)
        l_c["xaxis"].update(showgrid=False, showticklabels=False)
        l_c["yaxis"].update(tickfont=dict(color="#94a3b8", size=12))
        fig_c.update_layout(**l_c)
        st.plotly_chart(fig_c, use_container_width=True, config={"displayModeBar": False})

# ════════════════════════════════ TAB 3 ══════════════════════════════════════
with tab3:
    c_prod, c_canal = st.columns(2)

    with c_prod:
        por_prod = df_at.groupby("produto")["valor"].sum().reset_index().sort_values("valor", ascending=True)
        fig_p = go.Figure(go.Bar(
            x=por_prod["valor"], y=por_prod["produto"], orientation="h",
            marker=dict(color=COLORS[:len(por_prod)], line=dict(width=0)),
            text=[brl(v) for v in por_prod["valor"]],
            textposition="outside", textfont=dict(color="#94a3b8", size=11),
            hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>",
        ))
        l_p = plot_layout("Receita por Produto", height=300)
        l_p["xaxis"].update(showgrid=False, showticklabels=False)
        l_p["yaxis"].update(tickfont=dict(color="#94a3b8", size=12))
        fig_p.update_layout(**l_p)
        st.plotly_chart(fig_p, use_container_width=True, config={"displayModeBar": False})

    with c_canal:
        por_canal = df_at.groupby("canal").agg(deals=("valor","count"), receita=("valor","sum")).reset_index()
        fig_cn = go.Figure(go.Pie(
            labels=por_canal["canal"], values=por_canal["receita"],
            hole=0.55,
            marker=dict(colors=COLORS, line=dict(color=BG, width=2)),
            textinfo="percent+label", textfont=dict(size=11, color="white"),
            hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
        ))
        l_cn = plot_layout("Receita por Canal de Aquisição", height=300)
        l_cn.pop("xaxis",None); l_cn.pop("yaxis",None)
        l_cn["showlegend"] = False
        fig_cn.update_layout(**l_cn)
        st.plotly_chart(fig_cn, use_container_width=True, config={"displayModeBar": False})

    # Evolução produto ao longo do tempo
    df_prod_ev = df_at.copy()
    df_prod_ev["semana"] = df_prod_ev["data"].dt.to_period("W").dt.start_time
    prod_ev = df_prod_ev.groupby(["semana","produto"])["valor"].sum().reset_index()

    fig_pe = go.Figure()
    for i, prod in enumerate(df_at["produto"].unique()):
        d = prod_ev[prod_ev["produto"] == prod]
        fig_pe.add_trace(go.Scatter(
            x=d["semana"], y=d["valor"], name=prod, mode="lines+markers",
            line=dict(color=COLORS[i % len(COLORS)], width=2, shape="spline"),
            marker=dict(size=5),
            hovertemplate=f"<b>{prod}</b><br>%{{x|%d/%m/%Y}}<br>%{{y:,.0f}}<extra></extra>",
        ))
    l_pe = plot_layout("Evolução Semanal por Produto", height=300)
    l_pe["showlegend"] = True
    l_pe["legend"] = dict(font=dict(size=10, color="#94a3b8"), bgcolor="rgba(0,0,0,0)", orientation="h", x=0, y=-0.2)
    l_pe["yaxis"]["tickprefix"] = "R$ "
    fig_pe.update_layout(**l_pe)
    st.plotly_chart(fig_pe, use_container_width=True, config={"displayModeBar": False})

# ════════════════════════════════ TAB 4 ══════════════════════════════════════
with tab4:
    c_f1, c_f2, c_f3 = st.columns([2, 2, 1])
    with c_f1:
        prod_sel = st.multiselect("Produto", options=sorted(df["produto"].unique()), default=sorted(df["produto"].unique()), key="prod_tab4")
    with c_f2:
        canal_sel = st.multiselect("Canal", options=sorted(df["canal"].unique()), default=sorted(df["canal"].unique()), key="canal_tab4")
    with c_f3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        csv = df_at.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Exportar CSV", data=csv,
                           file_name=f"vendas_{datetime.today().strftime('%Y%m%d')}.csv",
                           mime="text/csv", use_container_width=True)

    df_tab = df_at[df_at["produto"].isin(prod_sel) & df_at["canal"].isin(canal_sel)].copy()
    df_tab = df_tab.sort_values("data", ascending=False)
    df_tab["data_fmt"] = df_tab["data"].dt.date

    st.markdown(f'<div class="section-label">{len(df_tab)} negócios encontrados · {brl(df_tab["valor"].sum())} em receita</div>', unsafe_allow_html=True)

    st.dataframe(
        df_tab[["data_fmt","vendedor","produto","canal","valor","dias_ciclo","status"]].rename(columns={
            "data_fmt":"Data","vendedor":"Vendedor","produto":"Produto",
            "canal":"Canal","valor":"Valor (R$)","dias_ciclo":"Ciclo (dias)","status":"Status"
        }),
        column_config={
            "Valor (R$)": st.column_config.ProgressColumn(
                "Valor", format="R$ %d",
                min_value=0, max_value=int(df_at["valor"].max()),
            ),
            "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "Ciclo (dias)": st.column_config.NumberColumn("Ciclo", format="%d dias"),
        },
        use_container_width=True, hide_index=True, height=420,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    💡 Este dashboard pode ser conectado ao seu banco de dados, CRM ou ERP &nbsp;·&nbsp;
    Feito por <a href="https://github.com/fabiicarniel" target="_blank">Octolab</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/fabiicarniel/octolab-sales-dashboard" target="_blank">Ver código no GitHub</a>
</div>
""", unsafe_allow_html=True)
