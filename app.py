import streamlit as st
import requests

API_URL = "https://automacao-p1-295355359739.southamerica-east1.run.app"

st.set_page_config(page_title="Sistema IA de Editais", layout="wide")

st.title("📊 Sistema IA de Análise de Editais")
st.write("Envie os arquivos do edital para análise completa.")

# =========================
# 10 CAMPOS DE UPLOAD
# =========================

st.subheader("📄 Arquivo 1")
arq1 = st.file_uploader("Selecione o arquivo", type=["pdf"], key="arq1")

st.subheader("📄 Arquivo 2")
arq2 = st.file_uploader("Selecione o arquivo", type=["pdf"], key="arq2")

st.subheader("📄 Arquivo 3")
arq3 = st.file_uploader("Selecione o arquivo", type=["pdf"], key="arq3")

st.subheader("📄 Arquivo 4")
arq4 = st.file_uploader("Selecione o arquivo", type=["pdf"], key="arq4")

st.subheader("📄 Arquivo 5")
arq5 = st.file_uploader("Selecione o arquivo", type=["pdf"], key="arq5")

st.subheader("📄 Arquivo 6")
arq6 = st.file_uploader("Selecione o arquivo", type=["pdf"], key="arq6")

st.subheader("📄 Arquivo 7")
arq7 = st.file_uploader("Selecione o arquivo", type=["pdf"], key="arq7")

st.subheader("📄 Arquivo 8")
arq8 = st.file_uploader("Selecione o arquivo", type=["pdf"], key="arq8")

st.subheader("📄 Arquivo 9")
arq9 = st.file_uploader("Selecione o arquivo", type=["pdf"], key="arq9")

st.subheader("📄 Arquivo 10")
arq10 = st.file_uploader("Selecione o arquivo", type=["pdf"], key="arq10")


# =========================
# BOTÃO
# =========================

if st.button("🚀 Analisar edital"):

    arquivos = [arq1, arq2, arq3, arq4, arq5, arq6, arq7, arq8, arq9, arq10]

    arquivos_validos = [a for a in arquivos if a is not None]

    if not arquivos_validos:
        st.error("Envie pelo menos um arquivo.")
    else:
        with st.spinner("Processando documentos..."):

            files = []

            for arq in arquivos_validos:
                files.append(("file", (arq.name, arq, "application/pdf")))

            try:
                response = requests.post(
                    f"{API_URL}/upload",
                    files=files,
                    timeout=300
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("✅ Upload e processamento concluídos!")
                    st.json(data)

                    edital_id = None

                    if "airtable" in data and data["airtable"]:
                        edital_id = data["airtable"].get("recordId")

                    if edital_id:
                        st.info(f"Edital criado: {edital_id}")

                        with st.spinner("Executando análise completa..."):
                            requests.post(f"{API_URL}/itens/{edital_id}", timeout=300)
                            requests.post(f"{API_URL}/regras/{edital_id}", timeout=300)
                            requests.post(f"{API_URL}/match/{edital_id}", timeout=300)
                            requests.post(f"{API_URL}/score/{edital_id}", timeout=300)

                        st.success("✅ Análise completa finalizada!")

                        st.markdown(
                            f"[📥 Baixar Excel](https://automacao-p1-295355359739.southamerica-east1.run.app/export/score/{edital_id})"
                        )
                    else:
                        st.warning("Upload feito, mas não retornou recordId.")

                else:
                    st.error(f"Erro na API: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error("Erro ao conectar com backend")
                st.text(str(e))
