import streamlit as st
from supabase import create_client, Client

# Código para esconder os menus e logos do Streamlit
esconder_menu = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(esconder_menu, unsafe_allow_html=True)


# ========================================================
# CONEXÃO COM O BANCO DE DADOS (SUPABASE)
# ========================================================
# Suas credenciais oficiais do projeto "Portal_Rocagem"

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Inicializa o cliente do banco de dados na nuvem
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ========================================================
# CONFIGURAÇÃO DA INTERFACE DO USUÁRIO (STREAMLIT)
# ========================================================
st.title("🌱 Portal Roçagem Saquarema")
st.subheader("Olá Claudio! Testando o banco de dados com Streamlit")

# Formulário para organizar os campos na tela
with st.form("formulario_orcamento"):
    txt_nome = st.text_input("Nome do Cliente", placeholder="Ex: Danilo")
    txt_whatsapp = st.text_input("WhatsApp", placeholder="Ex: 229098807")
    txt_terreno = st.number_input("Tamanho do Terreno (m²)", min_value=0, step=1)
    chk_lixo = st.checkbox("Com retirada de lixo?")
    
    # Botão para disparar o cálculo e o envio
    btn_enviar = st.form_submit_button("Calcular e Salvar no Banco")

# ========================================================
# LÓGICA DE PROCESSAMENTO E SALVAMENTO
# ========================================================
if btn_enviar:
    # Validação simples para não enviar campos em branco
    if not txt_nome or not txt_whatsapp or txt_terreno == 0:
        st.warning("⚠️ Por favor, preencha todos os campos do formulário!")
    else:
        try:
            # 1. Realiza o cálculo do orçamento (Ex: R$ 1,50 por m² + R$ 100 do lixo)
            valor_base = txt_terreno * 1.50
            adicional_lixo = 100.0 if chk_lixo else 0.0
            total = valor_base + adicional_lixo

            # 2. Insere os dados diretamente na tabela "orcamentos" do Supabase
            supabase.table("orcamentos").insert({
                "nome_cliente": txt_nome,
                "whatsapp": txt_whatsapp,
                "tamanho_terreno": txt_terreno,
                "com_retirada_lixo": chk_lixo,
                "valor_total": total
            }).execute()

            # 3. Exibe mensagem de sucesso na tela com o valor calculado
            st.success(f"✅ Sucesso! Orçamento de R$ {total:.2f} salvo no Supabase!")
            
        except Exception as erro:
            # Se houver algum erro de conexão, ele avisa na tela
            st.error(f"❌ Erro ao conectar ou salvar no banco: {erro}")
