import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_js_eval import streamlit_js_eval
from components.sidebar import render_sidebar

width = streamlit_js_eval(js_expressions='window.innerWidth')

is_mobile = width and width < 768
st.session_state["mobile"] = is_mobile

st.set_page_config(layout="centered")
st.title("📊 Dashboard Adaptativo de Planilhas")

arquivo = st.file_uploader("Envie qualquer arquivo Excel", type=["xlsx"])

if arquivo:

    try:
        df = pd.read_excel(arquivo)

        st.subheader("Preview dos Dados")
        st.dataframe(df, hide_index=True)

        # Detectar tipos automaticamente
        colunas_texto = df.select_dtypes(include=['object']).columns.tolist()        

        # 👇 Sidebar agora é componente
        tipo_grafico, eixo_x, eixo_y, filtros = render_sidebar(df, colunas_texto)

        # -------- Aplicar filtros --------

        df_filtrado = df.copy()

        for coluna, valores in filtros.items():
            df_filtrado = df_filtrado[df_filtrado[coluna].isin(valores)]

        # -------- KPIs --------

        if st.session_state.get("mobile", False):
            col1 = st.container()
            col2 = st.container()
        else:
            col1, col2 = st.columns(2)

        col1.metric("Total Registros", len(df_filtrado))
        col2.metric("Total Colunas", len(df_filtrado.columns))

        # -------- Gráficos --------

        if eixo_x:

            st.subheader("Visualização")

            if tipo_grafico == "Barra":

                if eixo_y != "Nenhum":
                    fig = px.bar(df_filtrado, x=eixo_x, y=eixo_y)
                else:
                    contagem = df_filtrado[eixo_x].value_counts().reset_index()
                    contagem.columns = [eixo_x, "Quantidade"]
                    fig = px.bar(contagem, x=eixo_x, y="Quantidade")

                st.plotly_chart(fig, use_container_width=True)

            elif tipo_grafico == "Pizza":

                contagem = df_filtrado[eixo_x].value_counts().reset_index()
                contagem.columns = [eixo_x, "Quantidade"]

                fig = px.pie(contagem, names=eixo_x, values="Quantidade")
                st.plotly_chart(fig, use_container_width=True)

            elif tipo_grafico == "Linha":

                if eixo_y != "Nenhum":
                    fig = px.line(df_filtrado, x=eixo_x, y=eixo_y)
                    st.plotly_chart(fig, use_container_width=True)

            elif tipo_grafico == "Histograma":

                fig = px.histogram(df_filtrado, x=eixo_x)
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
