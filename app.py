import streamlit as st
import requests

st.set_page_config(page_title="Sistema IA de Análise de Editais", layout="wide")

st.title("Sistema IA de Análise de Editais")
st.markdown("Envie os documentos do edital para análise completa.")

# Uploads
edital_file = st.file_uploader("1️⃣ Edital Principal (PDF)", type=["pdf"])
tr_file = st.file_uploader("2️⃣ Termo de Referência (PDF)", type=["pdf"])
documentos_complementares = st.file_uploader(
    "3️⃣ Documentos Complementares (opcional)",
    type=["pdf"],
    accept_multiple_files=True
)

# Botão
if st.button("Analisar edital"):

    if not edital_file or not tr_file:
        st.error("Envie o Edital e o Termo de Referência.")
        st.stop()

    files = []

    files.append(("file", (edital_file.name, edital_file, "application/pdf")))
    files.append(("file", (tr_file.name, tr_file, "application/pdf")))

    if documentos_complementares:
        for doc in documentos_complementares:
            files.append(("file", (doc.name, doc, "application/pdf")))

    url = "https://automacao-p1-295355359739.southamerica-east1.run.app/upload"

    with st.spinner("Processando análise..."):
        try:
            response = requests.post(url, files=files)

            try:
                data = response.json()
            except:
                data = response.text

            if response.status_code == 200:
                st.success("Análise concluída com sucesso")
                st.write(data)
            else:
                st.error(f"Erro no backend:\n{data}")

        except Exception as e:
            st.error(f"Erro ao conectar com backend: {e}")
