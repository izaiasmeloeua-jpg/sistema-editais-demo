import streamlit as st
import requests

st.set_page_config(page_title="Sistema IA de Editais", layout="wide")

st.title("📊 Sistema IA de Análise de Editais")
st.write("Envie os documentos do edital para análise completa.")

# =========================
# UPLOADS
# =========================

st.subheader("📄 1. Edital (PDF) *obrigatório*")
edital = st.file_uploader("Arraste ou selecione o EDITAL", type=["pdf"], key="edital")

st.subheader("📑 2. Termo de Referência (PDF) *obrigatório*")
tr = st.file_uploader("Arraste ou selecione o TR", type=["pdf"], key="tr")

st.subheader("📊 3. Escopo / Projeto")
escopo = st.file_uploader("Opcional", type=["pdf"], key="escopo")

st.subheader("📈 4. Cronograma")
cronograma = st.file_uploader("Opcional", type=["pdf"], key="cronograma")

st.subheader("💰 5. Orçamento")
orcamento = st.file_uploader("Opcional", type=["pdf"], key="orcamento")

st.subheader("📚 6. ETP / Estudos Técnicos")
etp = st.file_uploader("Opcional", type=["pdf"], key="etp")

st.subheader("📊 7. Planilha / Memória de Cálculo")
memoria = st.file_uploader("Opcional", type=["pdf"], key="memoria")


# =========================
# BOTÃO PRINCIPAL
# =========================

if st.button("🚀 Analisar edital"):

    if not edital or not tr:
        st.error("Envie pelo menos o EDITAL e o TERMO DE REFERÊNCIA.")
    else:
        with st.spinner("Processando documentos..."):

            files = []

            # obrigatórios
            files.append(("file", (edital.name, edital, "application/pdf")))
            files.append(("file", (tr.name, tr, "application/pdf")))

            # opcionais
            if escopo:
                files.append(("file", (escopo.name, escopo, "application/pdf")))

            if cronograma:
                files.append(("file", (cronograma.name, cronograma, "application/pdf")))

            if orcamento:
                files.append(("file", (orcamento.name, orcamento, "application/pdf")))

            if etp:
                files.append(("file", (etp.name, etp, "application/pdf")))

            if memoria:
                files.append(("file", (memoria.name, memoria, "application/pdf")))

            try:
                response = requests.post(
                    "https://automacao-p1-295355359739.southamerica-east1.run.app/upload",
                    files=files,
                    timeout=300
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("✅ Upload e processamento concluídos!")

                    st.json(data)

                else:
                    st.error(f"Erro na API: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error("Erro ao conectar com o backend")
                st.text(str(e))
