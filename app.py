import streamlit as st
import requests

API_URL = "https://automacao-p1-295355359739.southamerica-east1.run.app"

st.set_page_config(page_title="Sistema IA de Editais", layout="wide")

st.title("📊 Sistema IA de Análise de Editais")
st.write("Envie todos os arquivos do edital para análise completa.")

arquivos = st.file_uploader(
    "Arraste ou selecione TODOS os arquivos do edital (PDFs)",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("🚀 Analisar edital"):
    if not arquivos:
        st.error("Envie pelo menos um arquivo PDF.")
    else:
        with st.spinner("Processando documentos..."):
            files = []

            for arq in arquivos:
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

                        with st.spinner("Gerando itens, regras, match e score..."):
                            requests.post(f"{API_URL}/itens/{edital_id}", timeout=300)
                            requests.post(f"{API_URL}/regras/{edital_id}", timeout=300)
                            requests.post(f"{API_URL}/match/{edital_id}", timeout=300)
                            requests.post(f"{API_URL}/score/{edital_id}", timeout=300)

                        st.success("✅ Análise completa finalizada!")

                        st.markdown(
                            f"[📥 Baixar Excel](https://automacao-p1-295355359739.southamerica-east1.run.app/export/score/{edital_id})"
                        )
                    else:
                        st.warning("Upload concluído, mas não foi possível identificar o recordId do edital.")

                else:
                    st.error(f"Erro na API: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error("Erro ao conectar com o backend")
                st.text(str(e))
