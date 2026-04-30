import streamlit as st
import requests

API_URL = "https://automacao-p1-295355359739.southamerica-east1.run.app"

st.set_page_config(page_title="Sistema IA de Editais", layout="wide")
st.title("📊 Sistema IA de Análise de Editais")
st.write("Análise automatizada de editais em um único clique.")

if "edital_id" not in st.session_state:
    st.session_state.edital_id = None

def chamar_post(url, files=None):
    try:
        if files:
            r = requests.post(url, files=files, timeout=1800)
        else:
            r = requests.post(url, timeout=1800)
        try:
            return r.status_code, r.json()
        except:
            return r.status_code, r.text
    except Exception as e:
        return None, str(e)

# ======================
# UPLOAD
# ======================

st.subheader("📂 Upload dos arquivos")

arq1 = st.file_uploader("Arquivo 1", type=["pdf"], key="arq1")
arq2 = st.file_uploader("Arquivo 2", type=["pdf"], key="arq2")
arq3 = st.file_uploader("Arquivo 3", type=["pdf"], key="arq3")
arq4 = st.file_uploader("Arquivo 4", type=["pdf"], key="arq4")
arq5 = st.file_uploader("Arquivo 5", type=["pdf"], key="arq5")
arq6 = st.file_uploader("Arquivo 6", type=["pdf"], key="arq6")
arq7 = st.file_uploader("Arquivo 7", type=["pdf"], key="arq7")
arq8 = st.file_uploader("Arquivo 8", type=["pdf"], key="arq8")
arq9 = st.file_uploader("Arquivo 9", type=["pdf"], key="arq9")
arq10 = st.file_uploader("Arquivo 10", type=["pdf"], key="arq10")

arquivos = [arq1, arq2, arq3, arq4, arq5, arq6, arq7, arq8, arq9, arq10]
arquivos_validos = [a for a in arquivos if a is not None]

st.markdown("---")

# ======================
# BOTÃO PRINCIPAL
# ======================

if st.button("🚀 Analisar edital"):
    if not arquivos_validos:
        st.error("Envie pelo menos um arquivo.")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    # 1. Upload
    status.write("📤 Enviando arquivos...")
    files = [("file", (a.name, a, "application/pdf")) for a in arquivos_validos]
    code, data = chamar_post(f"{API_URL}/upload", files=files)

    if code != 200:
        st.error("Erro no upload")
        st.write(data)
        st.stop()

    edital_id = None
    if isinstance(data, dict):
        edital_id = data.get("recordId") or data.get("airtable", {}).get("recordId")

    if not edital_id:
        st.error("Não foi possível identificar o edital.")
        st.write(data)
        st.stop()

    st.session_state.edital_id = edital_id
    progress.progress(20)

    # 2. Itens
    status.write("🧠 Gerando itens...")
    chamar_post(f"{API_URL}/itens/{edital_id}")
    progress.progress(40)

    # 3. Regras
    status.write("⚙️ Gerando regras...")
    chamar_post(f"{API_URL}/regras/{edital_id}")
    progress.progress(60)

    # 4. Match
    status.write("🔗 Cruzando dados...")
    chamar_post(f"{API_URL}/match/{edital_id}")
    progress.progress(80)

    # 5. Score
    status.write("📊 Calculando score...")
    code, data = chamar_post(f"{API_URL}/score/{edital_id}")
    progress.progress(100)

    if code == 200:
        st.success("✅ Análise concluída!")

        st.subheader("📌 Decisão Estratégica")
        st.markdown(f"## {data.get('decisao_estrategica')}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Score Atual", data.get("score_atual"))
        col2.metric("Score Máximo", data.get("score_maximo_possivel"))
        col3.metric("Potencial", data.get("potencial_fechamento"))

        st.markdown("---")

        st.subheader("🧠 Resumo Executivo")
        st.write(data.get("resumo_executivo"))

        st.markdown("---")

        excel_url = f"{API_URL}/export/score/{edital_id}"
        st.markdown(f"[📥 Baixar Relatório em Excel]({excel_url})")

    else:
        st.error("Erro ao calcular score")
        st.write(data)
