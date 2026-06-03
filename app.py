import streamlit as st
import requests
import re
from datetime import datetime

API_URL = "https://sheetdb.io/api/v1/tn8m9exdlj62v"

st.set_page_config(
    page_title="Solicitação de Nota Fiscal",
    page_icon="📄",
    layout="centered"
)

# ==========================
# ESTILO
# ==========================

st.markdown("""
<style>

h1 {
    color: #7C5AC7;
    text-align: center;
    font-size: 34px;
}

.stButton > button {
    background-color: #A78BFA;
    color: white;
    border-radius: 10px;
    border: none;
    height: 45px;
    width: 100%;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #8B5CF6;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# FUNÇÕES
# ==========================

def validar_email(email):
    padrao = r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'
    return re.match(padrao, email)

def validar_cnpj(cnpj):
    numeros = re.sub(r'\\D', '', cnpj)
    return len(numeros) == 14

def gerar_protocolo():

    hoje = datetime.now().strftime("%Y%m%d")

    try:

        resposta = requests.get(API_URL)
        dados = resposta.json()

        protocolos_hoje = [
            item.get("Protocolo", "")
            for item in dados
            if hoje in item.get("Protocolo", "")
        ]

        sequencia = len(protocolos_hoje) + 1

    except:

        sequencia = 1

    return f"NF-{hoje}-{sequencia:03d}"

# ==========================
# CABEÇALHO
# ==========================

st.markdown(
    "<h1>📄 Solicitação de Nota Fiscal</h1>",
    unsafe_allow_html=True
)

st.markdown("""
Preencha os dados abaixo para solicitar emissão, correção ou ajuste de nota fiscal.
""")

st.divider()

# ==========================
# DADOS DA EMPRESA
# ==========================

st.subheader("Dados da Empresa")

empresa = st.text_input(
    "Nome da Empresa *"
)

cnpj = st.text_input(
    "CNPJ *",
    placeholder="Ex.: 12.345.678/0001-90"
)

email = st.text_input(
    "E-mail para acompanhamento *",
    placeholder="Ex.: financeiro@empresa.com.br"
)

# ==========================
# DADOS DA SOLICITAÇÃO
# ==========================

st.subheader("Dados da Solicitação")

meses = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro"
]

competencias = []

for ano in [2026, 2027]:
    for mes in meses:
        competencias.append(f"{mes}/{ano}")

competencia = st.selectbox(
    "Competência *",
    competencias,
    index=5
)

valor_psd = st.number_input(
    "Valor para emissão Pés sem Dor",
    min_value=0.0,
    format="%.2f"
)

valor_tc = st.number_input(
    "Valor para emissão TC Palmilhas",
    min_value=0.0,
    format="%.2f"
)

observacoes = st.text_area(
    "Observações / Solicitação Especial"
)

st.write("")

# ==========================
# BOTÃO
# ==========================

if st.button("📤 Enviar Solicitação"):

    erros = []

    if not empresa.strip():
        erros.append("Nome da Empresa")

    if not validar_cnpj(cnpj):
        erros.append("CNPJ válido")

    if not validar_email(email):
        erros.append("E-mail válido")

    if erros:

        st.error(
            "Preencha corretamente os seguintes campos:\n\n- "
            + "\n- ".join(erros)
        )

    else:

        protocolo = gerar_protocolo()

        dados = {
            "data": [{
                "Protocolo": protocolo,
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Empresa": empresa,
                "CNPJ": cnpj,
                "Email": email,
                "Competencia": competencia,
                "Valor PSD": valor_psd,
                "Valor TC": valor_tc,
                "Observacoes": observacoes,
                "Status": "Recebida"
            }]
        }

        resposta = requests.post(API_URL, json=dados)

        if resposta.status_code in [200, 201]:

            st.success(
                f"""
✅ Solicitação enviada com sucesso!

Protocolo: {protocolo}

Guarde este número para futuras consultas.
"""
            )

        else:

            st.error(
                "Erro ao enviar a solicitação. Tente novamente."
            )

# ==========================
# RODAPÉ
# ==========================

st.divider()

st.caption(
    "Em caso de dúvidas, entre em contato com a equipe fiscal."
)
