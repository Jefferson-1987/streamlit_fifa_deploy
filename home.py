import streamlit as st
<<<<<<< HEAD
import webbrowser
import pandas as pd
from datetime import datetime 

if "data" not in st.session_state:
    df_data = pd.read_csv("datasets/CLEAN_FIFA23_official_data.csv", index_col=0)
    df_data = df_data[df_data["Contract Valid Until"] >= datetime.today().year]
    df_data = df_data[df_data["Value(£)"] > 0]
    df_data = df_data.sort_values(by="Overall", ascending=False)
    st.session_state["data"] = df_data

st.markdown("# FIFA23 OFFICIAL DATASET! ⚽️")
st.sidebar.markdown("Desenvolvido por [Jefferson](https://github.com/Jefferson-1987/streamlit_fifa_deploy/blob/main/home.py)")


btn = st.button("Acesse os dados no Kaggle")
if btn:
    webbrowser.open_new_tab("https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data")

st.markdown(
    """
    O conjunto de dados
    de jogadores de futebol de 2017 a 2023 fornece informações 
    abrangentes sobre jogadores de futebol profissionais.
    O conjunto de dados contém uma ampla gama de atributos, incluindo dados demográficos 
    do jogador, características físicas, estatísticas de jogo, detalhes do contrato e 
    afiliações de clubes. 
    
    Com **mais de 17.000 registros**, este conjunto de dados oferece um recurso valioso para 
    analistas de futebol, pesquisadores e entusiastas interessados em explorar vários 
    aspectos do mundo do futebol, pois permite estudar atributos de jogadores, métricas de 
    desempenho, avaliação de mercado, análise de clubes, posicionamento de jogadores e 
    desenvolvimento do jogador ao longo do tempo.
"""
)
=======
import asyncio
import asyncpg
from datetime import datetime

# Configurações do Banco de Dados PostgreSQL
DB_USER = "seu_usuario"
DB_PASSWORD = "sua_senha"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "seu_banco"

# Função para conectar ao PostgreSQL com asyncpg
@st.cache_resource
def get_connection():
    return asyncio.run(asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    ))

# Streamlit App
st.title("Recebimento de Arquivos .txt com PostgreSQL (asyncpg)")

# Conexão ao banco
conn = get_connection()

# Criar tabela (se não existir)
async def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS arquivos (
        id SERIAL PRIMARY KEY,
        nome_arquivo TEXT NOT NULL,
        conteudo TEXT NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    await conn.execute(query)

asyncio.run(create_table())

# Upload de arquivo
uploaded_file = st.file_uploader("Faça upload do arquivo .txt", type="txt")

if uploaded_file:
    file_name = uploaded_file.name
    file_content = uploaded_file.read().decode("utf-8")

    async def save_file():
        query = """
        INSERT INTO arquivos (nome_arquivo, conteudo, data_criacao)
        VALUES ($1, $2, $3)
        """
        await conn.execute(query, file_name, file_content, datetime.utcnow())

    asyncio.run(save_file())
    st.success(f"Arquivo '{file_name}' salvo com sucesso no banco de dados!")

# Listar arquivos
st.subheader("Arquivos Salvos:")
async def fetch_files():
    query = "SELECT id, nome_arquivo, data_criacao FROM arquivos"
    return await conn.fetch(query)

rows = asyncio.run(fetch_files())

if rows:
    for row in rows:
        st.write(f"📄 **{row['nome_arquivo']}** (Enviado em: {row['data_criacao']})")
        st.download_button(
            label=f"Baixar {row['nome_arquivo']}",
            data=row['conteudo'],
            file_name=row['nome_arquivo'],
            mime="text/plain"
        )
else:
    st.write("Nenhum arquivo salvo no banco de dados ainda.")
>>>>>>> bc3c96ea31eba53ab7dfc09a210429b4c091535b
