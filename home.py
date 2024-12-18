import psycopg2
import streamlit as st
from datetime import datetime

# Configurações do Banco de Dados PostgreSQL
DB_USER = "seu_usuario"
DB_PASSWORD = "sua_senha"
DB_HOST = "localhost"  # IP ou hostname do servidor PostgreSQL
DB_PORT = "5432"  # Porta padrão do PostgreSQL
DB_NAME = "seu_banco"

# Função para conectar ao banco de dados
@st.cache_resource
def get_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# Conexão com o banco
conn = get_connection()
cursor = conn.cursor()

# Criar tabela (se não existir)
cursor.execute("""
CREATE TABLE IF NOT EXISTS arquivos (
    id SERIAL PRIMARY KEY,
    nome_arquivo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Streamlit App
st.title("Recebimento de Arquivos .txt com PostgreSQL (psycopg2)")

# Upload de arquivo
uploaded_file = st.file_uploader("Faça upload do arquivo .txt", type="txt")

if uploaded_file:
    # Nome e conteúdo do arquivo
    file_name = uploaded_file.name
    file_content = uploaded_file.read().decode("utf-8")

    # Salvar no banco de dados
    cursor.execute("""
    INSERT INTO arquivos (nome_arquivo, conteudo, data_criacao)
    VALUES (%s, %s, %s)
    """, (file_name, file_content, datetime.utcnow()))
    conn.commit()
    st.success(f"Arquivo '{file_name}' salvo com sucesso no banco de dados!")

# Listar arquivos armazenados
st.subheader("Arquivos Salvos:")
cursor.execute("SELECT id, nome_arquivo, data_criacao FROM arquivos")
rows = cursor.fetchall()

if rows:
    for row in rows:
        file_id, file_name, file_date = row
        st.write(f"📄 **{file_name}** (Enviado em: {file_date})")
        
        # Botão para baixar o arquivo
        cursor.execute("SELECT conteudo FROM arquivos WHERE id = %s", (file_id,))
        file_content = cursor.fetchone()[0]
        st.download_button(
            label=f"Baixar {file_name}",
            data=file_content,
            file_name=file_name,
            mime="text/plain"
        )
else:
    st.write("Nenhum arquivo salvo no banco de dados ainda.")
