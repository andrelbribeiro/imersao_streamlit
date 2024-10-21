import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards


@st.cache_data
def carregar_dados():
    
    df = pd.read_excel("Vendas.xlsx")

    return df

def main():
    st.set_page_config(layout="wide")
    
    st.sidebar.image("f3.png", width=100)

    st.title("Dashboard de Vendas 🅰️")
    col1, col2, col3 = st.columns(3)

    df = carregar_dados()

    ano_filtrado = st.sidebar.selectbox("Filtrar por Ano:", ["Todos", *df["Ano"].unique()])

    # Aplicar filtro apenas se não for todos
    if ano_filtrado != "Todos":
        df_filtrado = df[df["Ano"] == ano_filtrado]
    else:
        df_filtrado = df

    total_custo = df_filtrado['Custo'].sum().astype(str)
    total_custo = total_custo.replace(".", ",")
    total_custo = "R$ " + total_custo[0:2] + "." + total_custo[2:5] + "." + total_custo[5:]
    #total_custo = (df_filtrado["Custo"].sum())
    #total_custo = f"R$ {total_custo:,.2f}"


    total_lucro = df_filtrado['Lucro'].sum().astype(str)
    total_lucro = total_lucro.replace(".", ",")
    total_lucro = "R$ " + total_lucro[0:2] + "." + total_lucro[2:5] + "." + total_lucro[5:11]
    #total_lucro = (df_filtrado["Lucro"].sum())
    #total_lucro = f"R$ {total_lucro:,.2f}"
    
    total_clientes = df_filtrado["ID Cliente"].nunique()

    with col1:
        st.metric("Total Custo",total_custo)
        style_metric_cards(border_left_color="#3e4095")

    with col2:
        st.metric("Total Lucro", total_lucro)

    with col3:
       st.metric("Total Cliente",total_clientes)

    
    st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 18px;
        color: rgba(0,0,0,0,)
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    col3, col4 = st.columns(2)


    produtos_vendidos_marca = df_filtrado.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()
    fig = px.bar(produtos_vendidos_marca, x='Quantidade', y='Marca', orientation='h', title='Total Produtos Vendidos por Marca',
             color_discrete_sequence=["#3e4095"], text='Quantidade')
    fig.update_layout(title_x=0.5)
    col3.plotly_chart(fig, use_container_width=True)

    lucro_categoria = df_filtrado.groupby("Categoria")["Lucro"].sum().reset_index()
    lucro_mes_categoria = df_filtrado.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()
    
    fig2 = px.pie(lucro_categoria, values='Lucro', names='Categoria', title='Lucro por Categoria', hole=0.5)
    col4.plotly_chart(fig2, use_container_width=True)

    fig3 = px.line(lucro_mes_categoria, x="mes_ano", y="Lucro", title='Lucro x Mês x Categoria', color="Categoria", markers=True)
    st.plotly_chart(fig3)

if __name__ == "__main__":

    main()