import streamlit as st
import requests

# URL do seu sistema (Cloud Run)
API_URL = "https://automacao-p1-gmld6pkskq-rj.a.run.app"

st.set_page_config(page_title="Sistema IA de Editais", layout="wide")

st.title("📄 Sistema IA de Análise de Editais")

st.markdown("Envie um edital em PDF e obtenha análise automática com score e recomendação estratégica.")

uploaded_file = st.file_uploader("📎 Enviar edital (PDF)", type=["pdf"])

if uploaded_file:
    st.success("Arquivo carregado com sucesso!")

    if st.button("🚀 Analisar edital"):
        with st.spinner("Processando edital..."):
            
            # Upload do arquivo
            files = {"file": uploaded_file.getvalue()}
            response_upload = requests.post(f"{API_URL}/upload", files=files)

            if response_upload.status_code != 200:
                st.error("Erro no upload do edital.")
            else:
                data = response_upload.json()
                edital_id = data.get("edital_id")

                st.info(f"Edital processado: {edital_id}")

                # Gerar relatório
                response_relatorio = requests.get(f"{API_URL}/relatorio/{edital_id}")

                if response_relatorio.status_code == 200:
                    st.subheader("📊 Resultado da Análise")
                    st.text(response_relatorio.text)

                    # Botão para exportar Excel
                    excel_url = f"{API_URL}/export/score/{edital_id}"
                    st.markdown(f"[📥 Baixar Excel]({excel_url})")

                else:
                    st.error("Erro ao gerar relatório.")
