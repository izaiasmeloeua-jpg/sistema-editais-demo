import streamlit as st
import requests

API_URL = "https://automacao-p1-295355359739.southamerica-east1.run.app"

st.set_page_config(page_title="Sistema IA de Editais", layout="wide")

st.title("📊 Sistema IA de Análise de Editais")

# uploads
arquivos = []
for i in range(1, 11):
    arquivos.append(
        st.file_uploader(f"Arquivo {i}", type=["pdf"], key=f"arq{i}")
    )

if st.button("🚀 Analisar edital"):

    arquivos_validos = [a for a in arquivos if a]

    if not arquivos_validos:
        st.error("Envie pelo menos um arquivo.")
    else:
        files = [("file", (a.name, a, "application/pdf")) for a in arquivos_validos]

        try:
            # STEP 1 - upload
            upload = requests.post(f"{API_URL}/upload", files=files, timeout=300)
            st.write("UPLOAD:", upload.status_code)

            data = upload.json()
            st.json(data)

            edital_id = data.get("recordId") or data.get("airtable", {}).get("recordId")

            st.write("ID:", edital_id)

            if not edital_id:
                st.error("Não encontrou recordId")
                st.stop()

            # STEP 2 - itens
            r1 = requests.post(f"{API_URL}/itens/{edital_id}", timeout=300)
            st.write("ITENS:", r1.status_code, r1.text)

            # STEP 3 - regras
            r2 = requests.post(f"{API_URL}/regras/{edital_id}", timeout=300)
            st.write("REGRAS:", r2.status_code)

            # STEP 4 - match
            r3 = requests.post(f"{API_URL}/match/{edital_id}", timeout=300)
            st.write("MATCH:", r3.status_code)

            # STEP 5 - score
            r4 = requests.post(f"{API_URL}/score/{edital_id}", timeout=300)
            st.write("SCORE:", r4.status_code)

            st.success("Finalizado")

        except Exception as e:
            st.error(str(e))
