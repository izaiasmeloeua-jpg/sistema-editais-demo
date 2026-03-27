import streamlit as st
import requests

API_URL = "https://automacao-p1-295355359739.southamerica-east1.run.app"

st.set_page_config(page_title="Sistema IA de Editais", layout="wide")
st.title("📊 Sistema IA de Análise de Editais")
st.write("Fluxo controlado da análise do edital.")

if "edital_id" not in st.session_state:
    st.session_state.edital_id = None

if "upload_ok" not in st.session_state:
    st.session_state.upload_ok = False

if "itens_ok" not in st.session_state:
    st.session_state.itens_ok = False

if "regras_ok" not in st.session_state:
    st.session_state.regras_ok = False

if "match_ok" not in st.session_state:
    st.session_state.match_ok = False

if "score_ok" not in st.session_state:
    st.session_state.score_ok = False


def chamar_post(url):
    try:
        r = requests.post(url, timeout=300)
        try:
            data = r.json()
        except Exception:
            data = r.text
        return r.status_code, data
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

if st.button("1️⃣ Criar edital / Fazer upload"):
    if not arquivos_validos:
        st.error("Envie pelo menos um arquivo.")
    else:
        with st.spinner("Enviando arquivos e criando edital..."):
            files = [("file", (a.name, a, "application/pdf")) for a in arquivos_validos]

            try:
                response = requests.post(f"{API_URL}/upload", files=files, timeout=300)

                try:
                    data = response.json()
                except Exception:
                    data = response.text

                if response.status_code == 200:
                    edital_id = None
                    if isinstance(data, dict):
                        edital_id = data.get("recordId") or data.get("airtable", {}).get("recordId")

                    if edital_id:
                        st.session_state.edital_id = edital_id
                        st.session_state.upload_ok = True
                        st.session_state.itens_ok = False
                        st.session_state.regras_ok = False
                        st.session_state.match_ok = False
                        st.session_state.score_ok = False

                        st.success("✅ Edital criado com sucesso")
                        st.info(f"Record ID: {edital_id}")

                        if isinstance(data, dict):
                            extraido = data.get("extraido", {})
                            st.write("**Processo:**", extraido.get("processo_administrativo"))
                            st.write("**Concorrência:**", extraido.get("concorrencia_numero"))
                            st.write("**Valor estimado:**", extraido.get("valor_estimado_raw"))
                            st.write("**Data da sessão:**", extraido.get("data_sessao"))
                            st.write("**Arquivos processados:**", data.get("total_processado"))
                    else:
                        st.error("Upload funcionou, mas o recordId não foi encontrado.")
                        st.write(data)
                else:
                    st.error(f"Erro no upload: {response.status_code}")
                    st.write(data)

            except Exception as e:
                st.error("Erro ao conectar com o backend")
                st.text(str(e))

st.markdown("---")
st.subheader("⚙️ Etapas da análise")

if st.session_state.edital_id:
    st.write(f"**Edital atual:** {st.session_state.edital_id}")
else:
    st.warning("Nenhum edital criado ainda.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("2️⃣ Gerar itens", disabled=not st.session_state.upload_ok):
        with st.spinner("Gerando itens..."):
            status, data = chamar_post(f"{API_URL}/itens/{st.session_state.edital_id}")
            if status == 200:
                st.session_state.itens_ok = True
                st.success("✅ Itens gerados")
                st.write(data)
            else:
                st.error(f"Erro em /itens: {status}")
                st.write(data)

with col2:
    if st.button("3️⃣ Gerar regras", disabled=not st.session_state.itens_ok):
        with st.spinner("Gerando regras..."):
            status, data = chamar_post(f"{API_URL}/regras/{st.session_state.edital_id}")
            if status == 200:
                st.session_state.regras_ok = True
                st.success("✅ Regras geradas")
                st.write(data)
            else:
                st.error(f"Erro em /regras: {status}")
                st.write(data)

with col3:
    if st.button("4️⃣ Rodar match", disabled=not st.session_state.regras_ok):
        with st.spinner("Rodando match..."):
            status, data = chamar_post(f"{API_URL}/match/{st.session_state.edital_id}")
            if status == 200:
                st.session_state.match_ok = True
                st.success("✅ Match concluído")
                st.write(data)
            else:
                st.error(f"Erro em /match: {status}")
                st.write(data)

with col4:
    if st.button("5️⃣ Calcular score", disabled=not st.session_state.match_ok):
        with st.spinner("Calculando score..."):
            status, data = chamar_post(f"{API_URL}/score/{st.session_state.edital_id}")
            if status == 200:
                st.session_state.score_ok = True
                st.success("✅ Score calculado")
                st.write(data)
            else:
                st.error(f"Erro em /score: {status}")
                st.write(data)

st.markdown("---")
st.subheader("📥 Exportação")

if st.session_state.score_ok and st.session_state.edital_id:
    excel_url = f"{API_URL}/export/score/{st.session_state.edital_id}"
    st.markdown(f"[📊 Baixar Excel]({excel_url})")
else:
    st.info("O Excel será liberado após o score.")
