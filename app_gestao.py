import streamlit as st
import pandas as pd
import os

ARQUIVO = "solicitacoes.xlsx"

# ==========================
# CONFIGURAÇÃO
# ==========================

st.set_page_config(
    page_title="Gestão de Solicitações",
    page_icon="📋",
    layout="wide"
)

# ==========================
# LOGIN
# ==========================

USUARIO = "fiscal"
SENHA = "prado041"

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:

    st.title("🔒 Área de Gestão")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        if usuario == USUARIO and senha == SENHA:
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

    st.stop()

# ==========================
# ESTILO
# ==========================

st.markdown("""
<style>

h1 {
    color: #7C5AC7;
}

.stButton > button {
    background-color: #A78BFA;
    color: white;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# LEITURA DOS DADOS
# ==========================

def carregar_dados():

    if not os.path.exists(ARQUIVO):

        return pd.DataFrame(columns=[
            "Protocolo",
            "Data",
            "Empresa",
            "CNPJ",
            "Email",
            "Competencia",
            "Valor PSD",
            "Valor TC",
            "Observacoes",
            "Status"
        ])

    return pd.read_excel(ARQUIVO)

df = carregar_dados()

if len(df) == 0:

    st.title("📋 Gestão de Solicitações")
    st.info("Nenhuma solicitação encontrada.")
    st.stop()

# ==========================
# GARANTIR COLUNA STATUS
# ==========================

if "Status" not in df.columns:
    df["Status"] = "Recebida"

# ==========================
# CABEÇALHO
# ==========================

st.title("📋 Gestão de Solicitações")

# ==========================
# DASHBOARD
# ==========================

recebidas = len(df[df["Status"] == "Recebida"])
processo = len(df[df["Status"] == "Em Processo de Emissão"])
concluidas = len(df[df["Status"] == "Concluída"])

c1, c2, c3 = st.columns(3)

c1.metric("📥 Recebidas", recebidas)
c2.metric("🔄 Em Processo", processo)
c3.metric("✅ Concluídas", concluidas)

st.divider()

# ==========================
# FILTROS
# ==========================

empresas = ["Todas"] + sorted(df["Empresa"].astype(str).unique().tolist())

status_lista = [
    "Todos",
    "Recebida",
    "Em Processo de Emissão",
    "Concluída"
]

empresa_filtro = st.selectbox(
    "Empresa",
    empresas
)

status_filtro = st.selectbox(
    "Status",
    status_lista
)

df_filtrado = df.copy()

if empresa_filtro != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["Empresa"] == empresa_filtro
    ]

if status_filtro != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["Status"] == status_filtro
    ]

# ==========================
# TABELA
# ==========================

st.subheader("Solicitações")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# ==========================
# DETALHES
# ==========================

st.divider()

protocolos = df_filtrado["Protocolo"].tolist()

if len(protocolos) > 0:

    protocolo = st.selectbox(
        "Selecione uma solicitação",
        protocolos
    )

    linha = df[
        df["Protocolo"] == protocolo
    ].iloc[0]

    st.subheader("Detalhes")

    st.write(f"**Empresa:** {linha['Empresa']}")
    st.write(f"**CNPJ:** {linha['CNPJ']}")
    st.write(f"**E-mail:** {linha['Email']}")
    st.write(f"**Competência:** {linha['Competencia']}")
    st.write(f"**Valor PSD:** R$ {linha['Valor PSD']}")
    st.write(f"**Valor TC:** R$ {linha['Valor TC']}")
    st.write(f"**Observações:** {linha['Observacoes']}")

    novo_status = st.selectbox(
        "Alterar Status",
        [
            "Recebida",
            "Em Processo de Emissão",
            "Concluída"
        ],
        index=[
            "Recebida",
            "Em Processo de Emissão",
            "Concluída"
        ].index(linha["Status"])
        if linha["Status"] in [
            "Recebida",
            "Em Processo de Emissão",
            "Concluída"
        ]
        else 0
    )

    if st.button("Salvar Status"):

        df.loc[
            df["Protocolo"] == protocolo,
            "Status"
        ] = novo_status

        df.to_excel(
            ARQUIVO,
            index=False
        )

        st.success("Status atualizado com sucesso.")
        st.rerun()