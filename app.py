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
        except Exception:
            return r.status_code, r.text
    except Exception as e:
        return None, str(e)

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

if st.button("🚀 Analisar edital"):
    if not arquivos_validos:
        st.error("Envie pelo menos um arquivo.")
        st.stop()

    progress = st.progress(0)
    status_box = st.empty()

    status_box.write("📤 Enviando arquivos e criando edital...")
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
        st.error("Upload concluído, mas não foi possível identificar o edital.")
        st.write(data)
        st.stop()

    st.session_state.edital_id = edital_id
    progress.progress(20)

    status_box.write("🧠 Gerando itens do edital...")
    code, data_itens = chamar_post(f"{API_URL}/itens/{edital_id}")
    if code != 200:
        st.error("Erro ao gerar itens")
        st.write(data_itens)
        st.stop()
    progress.progress(40)

    status_box.write("⚙️ Gerando regras de análise...")
    code, data_regras = chamar_post(f"{API_URL}/regras/{edital_id}")
    if code != 200:
        st.error("Erro ao gerar regras")
        st.write(data_regras)
        st.stop()
    progress.progress(60)

    status_box.write("🔗 Cruzando requisitos com a base técnica...")
    code, data_match = chamar_post(f"{API_URL}/match/{edital_id}")
    if code != 200:
        st.error("Erro ao rodar match")
        st.write(data_match)
        st.stop()
    progress.progress(80)

    status_box.write("📊 Calculando score e decisão estratégica...")
    code, data_score = chamar_post(f"{API_URL}/score/{edital_id}")
    if code != 200:
        st.error("Erro ao calcular score")
        st.write(data_score)
        st.stop()
    progress.progress(100)

    status_box.empty()
    st.success("✅ Análise concluída com sucesso!")

    decisao = str(data_score.get("decisao_estrategica", "Análise concluída"))
    score_atual = data_score.get("score_atual", 0)
    score_maximo = data_score.get("score_maximo_possivel", 0)
    potencial = data_score.get("potencial_fechamento", 0)
    semaforo = str(data_score.get("semaforo", "")).upper()
    recomendacao = data_score.get("recomendacao_ia", "")
    resumo = data_score.get("resumo_executivo", "")

    st.markdown("---")
    st.subheader("📌 Decisão Estratégica")

    if "NÃO" in decisao.upper():
        st.error(f"🚫 {decisao}")
    elif "PARCEIRO" in decisao.upper() or "REFORÇO" in decisao.upper():
        st.warning(f"🤝 {decisao}")
    else:
        st.success(f"✅ {decisao}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score Atual", score_atual)
    col2.metric("Score Máximo", score_maximo)
    col3.metric("Potencial de Fechamento", potencial)
    col4.metric("Semáforo", semaforo)

    if recomendacao:
        st.info(f"💡 {recomendacao}")

    st.markdown("---")
    st.subheader("🧠 Resumo Executivo")

    if resumo:
        st.markdown(
            f"""
            <div style="font-size:16px; line-height:1.7;">
            {resumo.replace(chr(10), "<br>")}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write("Resumo executivo não disponível.")

    st.markdown("---")
    st.subheader("📥 Exportação")

    excel_url = f"{API_URL}/export/score/{edital_id}"
    st.markdown(f"[📊 Baixar Relatório em Excel]({excel_url})")
