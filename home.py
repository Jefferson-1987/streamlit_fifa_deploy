import streamlit as st
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Text, LargeBinary
import datetime

# Configuração do banco de dados
DB_USER = "seu_usuario"
DB_PASS = "sua_senha"
DB_HOST = "localhost"  # Ou URL do servidor remoto
DB_PORT = "5432"
DB_NAME = "seu_banco"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Conexão com o PostgreSQL usando SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Definição das tabelas
comentarios = Table(
    "comentarios", metadata,
    Column("id", Integer, primary_key=True),
    Column("conteudo", Text, nullable=False),
    Column("data_criacao", String, default=datetime.datetime.now)
)

arquivos = Table(
    "arquivos", metadata,
    Column("id", Integer, primary_key=True),
    Column("nome_arquivo", String, nullable=False),
    Column("conteudo", LargeBinary, nullable=False),
    Column("data_criacao", String, default=datetime.datetime.now)
)

# Garantir que as tabelas existem
metadata.create_all(engine)

# App Streamlit
st.title("Recebimento de Propostas com PostgreSQL")

# Seleção de opções
option = st.radio("Escolha uma opção:", ["Escrever comentário", "Enviar arquivo .txt"])

# Opção 1: Escrever comentário
if option == "Escrever comentário":
    comment = st.text_area("Escreva seu comentário:", height=200)
    if st.button("Salvar Comentário"):
        if comment.strip():
            with engine.connect() as conn:
                ins = comentarios.insert().values(conteudo=comment, data_criacao=str(datetime.datetime.now()))
                conn.execute(ins)
                st.success("Comentário salvo no banco de dados!")
        else:
            st.warning("O campo está vazio!")

# Opção 2: Enviar arquivo .txt
elif option == "Enviar arquivo .txt":
    uploaded_file = st.file_uploader("Escolha um arquivo .txt", type=["txt"])
    if uploaded_file is not None:
        file_content = uploaded_file.read()
        file_name = uploaded_file.name
        with engine.connect() as conn:
            ins = arquivos.insert().values(
                nome_arquivo=file_name,
                conteudo=file_content,
                data_criacao=str(datetime.datetime.now())
            )
            conn.execute(ins)
        st.success(f"Arquivo '{file_name}' salvo no banco de dados!")

# Visualizar comentários salvos
st.subheader("Comentários Salvos")
with engine.connect() as conn:
    result = conn.execute(comentarios.select())
    for row in result:
        st.write(f"**ID:** {row.id} - **Data:** {row.data_criacao}")
        st.write(f"📄 {row.conteudo}")
        st.write("---")

# Visualizar arquivos salvos
st.subheader("Arquivos Salvos")
with engine.connect() as conn:
    result = conn.execute(arquivos.select())
    for row in result:
        st.write(f"**ID:** {row.id} - **Nome:** {row.nome_arquivo} - **Data:** {row.data_criacao}")
        st.download_button(
            label=f"Baixar {row.nome_arquivo}",
            data=row.conteudo,
            file_name=row.nome_arquivo,
            mime="text/plain"
        )
