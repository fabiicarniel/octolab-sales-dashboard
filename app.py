import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Dashboard de Vendas", layout="wide", page_icon="📊")

st.markdown("""
    <style>
    .metric-card {
        background-color: #1e1e2e;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #7c3aed;
    }
    </style>
""", unsafe_allow_html=True)

# --- Dados fictícios ---
@st.cache_data
def gerar_dados():
    vendedores = ["Ana Paula", "Carlos Lima", "Fernanda Souza", "Ricardo Alves", "Juliana Costa"]
    produtos = ["Plano Starter", "Plano Pro", "Plano Enterprise", "Consultoria", "Suporte Premium"]
    status_opcoes = ["Fechado", "Fechado", "Fechado", "Em negociação", "Perdido"]

    random.seed(42)
    registros = []
    hoje = datetime.today()

    for i in range(300):
        data = hoje - timedelta(days=random.randint(0, 89))
        registros.append({
            "data": data,
            "vendedor": random.choice(vendedores),
            "produto": random.choice(produtos),
            "valor": random.randint(500, 15000),
            "status": random.choice(status_opcoes),
        })

    return pd.DataFrame(registros)

df = gerar_dados()
df_fechado = df[df["status"] == "Fechado"].copy()

# --- Sidebar ---
st.sidebar.image("https://via.placeholder.com/200x60?text=Octolab", use_container_width=True)
st.sidebar.markdown("### Filtros")

periodo = st.sidebar.selectbox("Período", ["Últimos 30 dias", "Últimos 60 dias", "Últimos 90 dias"])
dias = {"Últimos 30 dias": 30, "Últimos 60 dias": 60, "Últimos 90 dias": 90}[periodo]

vendedor_filtro = st.sidebar.multiselect(
    "Vendedor",
    options=df["vendedor"].unique(),
    default=df["vendedor"].unique()
)

corte = datetime.today() - timedelta(days=dias)
df_filtrado = df_fechado[
    (df_fechado["data"] >= corte) &
    (df_fechado["vendedor"].isin(vendedor_filtro))
]

# --- Header ---
st.title("📊 Dashboard de Vendas")
st.caption(f"Atualizado em {datetime.today().strftime('%d/%m/%Y às %H:%M')} · {periodo}")
st.divider()

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)

total_vendas = df_filtrado["valor"].sum()
qtd_deals = len(df_filtrado)
ticket_medio = df_filtrado["valor"].mean() if qtd_deals > 0 else 0

corte_anterior = corte - timedelta(days=dias)
df_anterior = df_fechado[
    (df_fechado["data"] >= corte_anterior) &
    (df_fechado["data"] < corte) &
    (df_fechado["vendedor"].isin(vendedor_filtro))
]
variacao = ((total_vendas - df_anterior["valor"].sum()) / df_anterior["valor"].sum() * 100) if len(df_anterior) > 0 else 0

col1.metric("💰 Receita Total", f"R$ {total_vendas:,.0f}".replace(",", "."), f"{variacao:+.1f}% vs período anterior")
col2.metric("🤝 Deals Fechados", qtd_deals)
col3.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.0f}".replace(",", "."))
col4.metric("👥 Vendedores Ativos", df_filtrado["vendedor"].nunique())

st.divider()

# --- Gráficos ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Receita por Vendedor")
    rank = df_filtrado.groupby("vendedor")["valor"].sum().reset_index().sort_values("valor", ascending=True)
    fig = px.bar(rank, x="valor", y="vendedor", orientation="h",
                 color="valor", color_continuous_scale="Purples",
                 labels={"valor": "Receita (R$)", "vendedor": ""})
    fig.update_layout(showlegend=False, coloraxis_showscale=False, plot_bgcolor="rgba(0,0,0,0)")
    fig.update_traces(texttemplate="R$ %{x:,.0f}", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.subheader("Receita por Produto")
    por_produto = df_filtrado.groupby("produto")["valor"].sum().reset_index()
    fig2 = px.pie(por_produto, names="produto", values="valor",
                  color_discrete_sequence=px.colors.sequential.Purples_r, hole=0.4)
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig2, use_container_width=True)

# --- Evolução temporal ---
st.subheader("Evolução de Receita")
df_filtrado["semana"] = df_filtrado["data"].dt.to_period("W").dt.start_time
evolucao = df_filtrado.groupby("semana")["valor"].sum().reset_index()
fig3 = px.area(evolucao, x="semana", y="valor",
               labels={"semana": "Semana", "valor": "Receita (R$)"},
               color_discrete_sequence=["#7c3aed"])
fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig3, use_container_width=True)

# --- Tabela ---
st.subheader("Últimas Vendas")
df_tabela = df_filtrado.sort_values("data", ascending=False).head(10).copy()
df_tabela["data"] = df_tabela["data"].dt.strftime("%d/%m/%Y")
df_tabela["valor"] = df_tabela["valor"].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))
st.dataframe(df_tabela.rename(columns={
    "data": "Data", "vendedor": "Vendedor",
    "produto": "Produto", "valor": "Valor", "status": "Status"
}), use_container_width=True, hide_index=True)

st.divider()
st.caption("💡 Este dashboard pode ser conectado ao seu banco de dados, CRM ou ERP. Feito por Octolab.")
