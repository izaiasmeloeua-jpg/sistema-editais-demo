import streamlit as st

st.set_page_config(page_title="Sistema IA de Editais", layout="wide")

st.title("📊 Sistema IA de Análise de Editais")
st.write("Envie os documentos do edital para análise completa.")

# 1. EDITAL
st.subheader("1️⃣ Edital (PDF) *obrigatório*")
edital = st.file_uploader(
    "Arraste ou selecione o EDITAL",
    type=["pdf"],
    key="edital"
)

# 2. TERMO DE REFERÊNCIA
st.subheader("2️⃣ Termo de Referência (PDF) *obrigatório*")
tr = st.file_uploader(
    "Arraste ou selecione o TERMO DE REFERÊNCIA",
    type=["pdf"],
    key="tr"
)

# 3. PONTUAÇÃO TÉCNICA
st.subheader("3️⃣ Pontuação Técnica (PDF)")
pontuacao = st.file_uploader(
    "Arraste ou selecione documento de PONTUAÇÃO",
    type=["pdf"],
    key="pontuacao"
)

# 4. ESCOPO / PROJETO
st.subheader("4️⃣ Escopo / Projeto (PDF)")
escopo = st.file_uploader(
    "Arraste ou selecione o ESCOPO",
    type=["pdf"],
    key="escopo"
)

# 5. MEMORIAL / ETP
st.subheader("5️⃣ Memorial / ETP (PDF)")
etp = st.file_uploader(
    "Arraste ou selecione o ETP ou MEMORIAL",
    type=["pdf"],
    key="etp"
)

# 6. PLANILHAS / ORÇAMENTO
st.subheader("6️⃣ Planilhas / Orçamento (PDF ou Excel)")
orcamento = st.file_uploader(
    "Arraste ou selecione PLANILHAS",
    type=["pdf", "xlsx", "xls"],
    key="orcamento"
)

# 7. CRONOGRAMA
st.subheader("7️⃣ Cronograma (PDF)")
cronograma = st.file_uploader(
    "Arraste ou selecione o CRONOGRAMA",
    type=["pdf"],
    key="cronograma"
)

# 8. OUTROS ANEXOS
st.subheader("8️⃣ Outros Anexos")
outros = st.file_uploader(
    "Arraste ou selecione outros documentos",
    type=["pdf"],
    accept_multiple_files=True,
    key="outros"
)

st.markdown("---")

if st.button("🚀 Analisar edital"):
    if not edital or not tr:
        st.error("Envie pelo menos o EDITAL e o TERMO DE REFERÊNCIA.")
    else:
        st.success("Arquivos recebidos com sucesso!")

        st.write("### 📂 Arquivos enviados:")
        st.write("Edital:", edital.name if edital else None)
        st.write("TR:", tr.name if tr else None)
        st.write("Pontuação:", pontuacao.name if pontuacao else None)
        st.write("Escopo:", escopo.name if escopo else None)
        st.write("ETP:", etp.name if etp else None)
        st.write("Orçamento:", orcamento.name if orcamento else None)
        st.write("Cronograma:", cronograma.name if cronograma else None)

        if outros:
            st.write("Outros anexos:")
            for f in outros:
                st.write("-", f.name)
