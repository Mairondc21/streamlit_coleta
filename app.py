import streamlit as st
import pandas as pd

with st.form("form"):
    st.write("Esse e meu questionario")
    meu_estado = st.selectbox(label="selecionar seu estado",options=["Rio de Janeiro","Minas gerais"])
    minha_area_atuacao = st.selectbox(label="Selecione sua area", options=["Data engenieer","data analitics","estagiario"])

    submitted = st.form_submit_button("submit")
    if submitted:
        st.write("slider",meu_estado, "checkbox", minha_area_atuacao)
        meu_dict = [{"meu_estado": meu_estado,
                    "minha_area_de_atuacao":minha_area_atuacao}]
        df = pd.DataFrame(meu_dict)

        df.to_csv("teste.csv")
