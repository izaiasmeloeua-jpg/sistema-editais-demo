import streamlit as st
import requests

st.set_page_config(page_title="Sistema IA de Análise de Editais", layout="wide")

st.title("📄 Sistema IA de Análise de Editais")
st.markdown("Envie os documentos do edital para análise completa.")

# =========================
# UPLOADS
# =========================
edital_file = st.file_uploader("1️⃣ Edital Principal (PDF)", type=["pdf"])
tr_file = st.file_uploader("2️⃣ Termo de Referência (PDF)", type=["pdf"])
documentos_complementares = st.file_uploader(
    "3️⃣ Documentos Complementares (opcional)",
    type=["pdf"],
    accept_multiple_files=True
)

# =========================
# BOTÃO
# =========================
if st.button("🚀 Analisar edital"):

    if not edital_file or not tr_file:
        st.error("Envie o Edital e o Termo de Referência.")
        st.stop()

    # =========================
    # MONTAR MULTIPART
    # =========================
    files = []

    # edital
    files.append(("files", (edital_file.name, edital_file, "application/pdf")))

    # TR
    files.append(("files", (tr_file.name, tr_file, "application/pdf")))

    # complementares
    if documentos_complementares:
        for doc in documentos_complementares:
            files.append(("files", (doc.name, doc, "application/pdf")))

    # =========================
    # CHAMADA BACKEND
    # =========================
    url = "https://automacao-p1-295355359739.southamerica-east1.run.app/upload"

    with st.spinner("Processando análise..."):
        try:
            response = requests.post(url, files=files)

            if response.status_code == 200:
                data = response.json()

                st.success("Análise concluída com sucesso!")

                st.markdown("## 📊 Resultado da Análise")
                st.json(data)

            else:
                st.error(f"Erro no backend: {response.text}")

        except Exception as e:
            st.error(f"Erro ao conectar com backend: {e}")
