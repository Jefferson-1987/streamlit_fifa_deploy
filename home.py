import streamlit as st
import webbrowser
import os
import pandas as pd
from datetime import datetime 


# Diretório para salvar os arquivos
SAVE_DIR = "uploads"

# Garantir que o diretório existe
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Título do app
st.title("Recebimento de Propostas")

# Campo para escolher entre texto ou upload
st.header("Submeta um comentário ou envie um arquivo .txt")

# Seleção: Comentário longo ou Upload
option = st.radio("Escolha uma opção:", ["Escrever comentário", "Enviar arquivo .txt"])

# Opção 1: Comentário longo
if option == "Escrever comentário":
    comment = st.text_area("Escreva seu comentário aqui:", height=200)
    
    if st.button("Salvar Comentário"):
        if comment.strip():
            # Criar um arquivo com data e hora
            file_name = f"comentario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            file_path = os.path.join(SAVE_DIR, file_name)
            
            # Salvar comentário em arquivo
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(comment)
            
            st.success(f"Comentário salvo com sucesso em `{file_name}`")
        else:
            st.warning("O campo de comentário está vazio. Por favor, escreva algo.")

# Opção 2: Enviar arquivo .txt
elif option == "Enviar arquivo .txt":
    uploaded_file = st.file_uploader("Escolha um arquivo .txt", type=["txt"])
    
    if uploaded_file is not None:
        file_name = f"arquivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = os.path.join(SAVE_DIR, file_name)
        
        # Salvar o arquivo no diretório de uploads
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Arquivo salvo com sucesso em `{file_name}`")

# Mensagem final
st.write("---")
st.write("Os arquivos são salvos na pasta `uploads` do projeto.")

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