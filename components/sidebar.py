import streamlit as st

def render_sidebar(df, colunas_texto):

    st.sidebar.title("Configuração")

    tipo_grafico = st.sidebar.selectbox(
        "Tipo de gráfico",
        ["Barra", "Pizza", "Linha", "Histograma"]
    )

    todas_colunas = df.columns.tolist()

    eixo_x = st.sidebar.selectbox("Eixo X", todas_colunas)
    eixo_y = st.sidebar.selectbox("Eixo Y (opcional)", ["Nenhum"] + todas_colunas)

    st.sidebar.header("Filtros")

    filtros = {}

    for coluna in colunas_texto:
        valores = st.sidebar.multiselect(
            f"Filtrar {coluna}",
            df[coluna].dropna().unique()
        )

        if valores:
            filtros[coluna] = valores

    return tipo_grafico, eixo_x, eixo_y, filtros
