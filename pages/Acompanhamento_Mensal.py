import pandas as pd
import streamlit as st


@st.cache_data
def carregar_dados():
    
    df = pd.read_excel("Vendas.xlsx")

    return df

def main():

    st.set_page_config(layout="wide")

    df = carregar_dados()

    MoM = df.groupby(["mes_ano"])["Lucro"].sum().reset_index()

    st.write(MoM)


if __name__ == "__main__":
    main()