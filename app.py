import streamlit as st
import requests

API_URL = "https://automacao-p1-295355359739.southamerica-east1.run.app"

st.set_page_config(page_title="Sistema IA de Editais", layout="wide")

st.title("📄 Sistema IA de Análise de Editais")
st.markdown("Envie os documentos do edital para análise completa.")

edital_file = st.file_uploader("1️⃣ Edital Principal (PDF)", type=["pdf"])
tr_file = st.file_uploader("2️⃣ Termo de Referência (PDF)", type=["pdf"])
anexos_files = st.file_uploader("3️⃣ Anexos (opcional)", type=["pdf"], accept_multiple_files=True)

if st.button("🚀 Analisar edital"):
    if not edital_file or not tr_file:
        st.error("Envie pelo menos o Edital e o Termo de Referência.")
    else:
        st.info("Processando...")

        files_to_send = [edital_file, tr_file]
        if anexos_files:
            files_to_send.extend(anexos_files)

        edital_id = None

        for f in files_to_send:
            response = requests.post(
                f"{API_URL}/upload",
                files={"file": (f.name, f, "application/pdf")}
            )

            if response.status_code != 200:
                st.error(f"Erro ao enviar {f.name}")
                st.stop()

            data = response.json()
            edital_id = data.get("editalId")

        if not edital_id:
            st.error("Não foi possível obter o ID do edital.")
            st.stop()

        for ep in ["itens", "regras", "match", "score"]:
            r = requests.post(f"{API_URL}/{ep}/{edital_id}")
            if r.status_code != 200:
                st.error(f"Erro na etapa: {ep}")
                st.stop()

        rel = requests.get(f"{API_URL}/relatorio/{edital_id}")

        if rel.status_code == 200:
            st.success("Análise concluída!")
            st.text(rel.text)

            excel_url = f"{API_URL}/export/score/{edital_id}"
            st.markdown(f"[📥 Baixar Excel]({excel_url})")
        else:
            st.error("Erro ao gerar relatório.")
