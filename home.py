import os
import streamlit as st

# Configurar o título do app
st.title("Recebimento de Arquivos .txt")

# Criar a pasta 'uploads' para salvar os arquivos (se não existir)
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Campo para fazer upload de arquivos
uploaded_file = st.file_uploader("Faça upload do arquivo .txt", type="txt")

if uploaded_file:
    # Nome e conteúdo do arquivo
    file_name = uploaded_file.name
    file_content = uploaded_file.read().decode("utf-8")  # Lê o conteúdo como texto
    
    # Salvar o arquivo na pasta 'uploads'
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)
    
    # Exibir sucesso e o conteúdo do arquivo
    st.success(f"Arquivo '{file_name}' salvo com sucesso!")
    st.text_area("Conteúdo do Arquivo:", file_content, height=300)

# Listar arquivos já enviados
st.subheader("Arquivos Salvos:")
saved_files = os.listdir(UPLOAD_FOLDER)
if saved_files:
    for saved_file in saved_files:
        st.write(saved_file)
else:
    st.write("Nenhum arquivo enviado ainda.")
