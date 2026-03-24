import streamlit as st

st.set_page_config(page_title="Sistema IA de Análise de Editais", layout="wide")

st.title("📄 Sistema IA de Análise de Editais")
st.markdown("Envie os documentos do edital para análise completa.")

# =========================
# 1️⃣ EDITAL PRINCIPAL
# =========================
edital_file = st.file_uploader(
    "1️⃣ Edital Principal (PDF)",
    type=["pdf"],
    accept_multiple_files=False
)

# =========================
# 2️⃣ TERMO DE REFERÊNCIA
# =========================
tr_file = st.file_uploader(
    "2️⃣ Termo de Referência (PDF)",
    type=["pdf"],
    accept_multiple_files=False
)

# =========================
# 3️⃣ DOCUMENTOS COMPLEMENTARES (MULTI)
# =========================
documentos_complementares = st.file_uploader(
    "3️⃣ Documentos Complementares (opcional)",
    type=["pdf"],
    accept_multiple_files=True
)

# =========================
# BOTÃO DE ANÁLISE
# =========================
if st.button("🚀 Analisar edital"):

    # Validação mínima
    if not edital_file or not tr_file:
        st.error("Por favor, envie o Edital Principal e o Termo de Referência.")
        st.stop()

    # Monta lista de arquivos
    files_to_send = [edital_file, tr_file]

    if documentos_complementares:
        files_to_send.extend(documentos_complementares)

    # Feedback visual
    st.success("Arquivos carregados com sucesso!")

    st.markdown("### 📦 Arquivos enviados:")
    for f in files_to_send:
        st.write(f"- {f.name}")

    # Simulação (depois conecta com backend)
    st.markdown("### 🤖 Processando análise...")
    st.info("Integração com o motor de análise será conectada aqui.")

    st.markdown("### 📊 Resultado")
    st.success("Estrutura pronta para análise completa do edital 🚀")
