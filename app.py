import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

def connect_to_db():
    engine = create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    return engine
class SurveyData(Base):
    __tablename__ = "survey_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    estado = Column(String(50))
    bibliotecas = Column(Text)
    area_atuacao = Column(String(50))
    horas_estudo = Column(String(20))
    conforto_dados = Column(String(50))
    experiencia_python = Column(Integer)
    experiencia_sql = Column(Integer)
    experiencia_cloud = Column(Integer)

def criar_tabela_se_nao_existir(engine):
    try:
        Base.metadata.create_all(engine)
    except SQLAlchemyError as e:
        st.error(f"Erro ao criar a tabela: {e}")

def salvar_dados_banco(session, dados):
    try:
        novo_dado = SurveyData(
            estado=dados["Estado"],
            bibliotecas=dados["Bibliotecas e ferramentas"],
            area_atuacao=dados["Área de Atuação"],
            horas_estudo=dados["Horas de Estudo"],
            conforto_dados=dados["Conforto com Dados"],
            experiencia_python=dados["Experiência de Python"],
            experiencia_sql=dados["Experiência de SQL"],
            experiencia_cloud=dados["Experiência de Cloud"],
        )
        session.add(novo_dado)
        session.commit()
    except SQLAlchemyError as e:
        st.error(f"Erro ao salvar os dados no banco de dados: {e}")
        session.rollback()


# Obter a instância do engine e criar a tabela se necessário
engine = connect_to_db()
if engine is not None:
    criar_tabela_se_nao_existir(engine)

# Configurar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)



# Opções de estados
estados = [
    "Acre",
    "Alagoas",
    "Amapá",
    "Amazonas",
    "Bahia",
    "Ceará",
    "Distrito Federal",
    "Espírito Santo",
    "Goiás",
    "Maranhão",
    "Mato Grosso",
    "Mato Grosso do Sul",
    "Minas Gerais",
    "Pará",
    "Paraíba",
    "Paraná",
    "Pernambuco",
    "Piauí",
    "Rio de Janeiro",
    "Rio Grande do Norte",
    "Rio Grande do Sul",
    "Rondônia",
    "Roraima",
    "Santa Catarina",
    "São Paulo",
    "Sergipe",
    "Tocantins",
]

# Opções de áreas de atuação
areas_atuacao = ["Analista de Dados", "Cientista de Dados", "Engenheiro de Dados"]

# Opções de bibliotecas
bibliotecas = [
    "Pandas",
    "Pydantic",
    "scikit-learn",
    "Git",
    "Pandera",
    "streamlit",
    "postgres",
    "databricks",
    "AWS",
    "Azure",
    "airflow",
    "dbt",
    "Pyspark",
    "Polars",
    "Kafka",
    "Duckdb",
    "PowerBI",
    "Excel",
    "Tableau",
    "storm",
]

# Opções de horas codando
horas_codando = ["Menos de 5", "5-10", "10-20", "Mais de 20"]

# Opções de conforto com dados
conforto_dados = ["Desconfortável", "Neutro", "Confortável", "Muito Confortável"]

# Criação do formulário
with st.form("dados_enquete"):
    estado = st.selectbox("Estado", estados)
    area_atuacao = st.selectbox("Área de Atuação", areas_atuacao)
    bibliotecas_selecionadas = st.multiselect(
        "Bibliotecas e ferramentas mais utilizadas", bibliotecas
    )
    horas_codando = st.selectbox("Horas Codando ao longo da semana", horas_codando)
    conforto_dados = st.selectbox(
        "Conforto ao programar e trabalhar com dados", conforto_dados
    )
    experiencia_python = st.slider("Experiência de Python", 0, 10)
    experiencia_sql = st.slider("Experiência de SQL", 0, 10)
    experiencia_cloud = st.slider("Experiência em Cloud", 0, 10)

    # Botão para submeter o formulário
    submit_button = st.form_submit_button("Enviar")

# Se o botão foi clicado, salvar os dados no DataFrame e no CSV
if submit_button:
    novo_dado = {
        "Estado": estado,
        "Bibliotecas e ferramentas": ", ".join(bibliotecas_selecionadas),
        "Área de Atuação": area_atuacao,
        "Horas de Estudo": horas_codando,
        "Conforto com Dados": conforto_dados,
        "Experiência de Python": experiencia_python,
        "Experiência de SQL": experiencia_sql,
        "Experiência de Cloud": experiencia_cloud,
    }
    session = Session()
    salvar_dados_banco(session, novo_dado)
    st.success("Dados enviados com sucesso!")

    # Verificar se o arquivo existe antes de tentar ler

st.write("Outside the form")
