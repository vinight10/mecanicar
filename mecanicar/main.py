import streamlit as st
import pandas as pd
import sqlite3 
from db_funcs import *
from PIL import Image
import time
import os
import shutil

# Função para verificar se o banco de dados já existe
def database_exists(db_path):
    return os.path.exists(db_path)

# Função para criar o banco de dados, se necessário
def create_database(db_path):
    if not database_exists(db_path):
        conn = sqlite3.connect(db_path)
        create_table()
        conn.close()

# Caminho absoluto para o banco de dados
DB_PATH = "mecanicar/database.db"

# Criar o banco de dados, se necessário
create_database(DB_PATH)

# Definindo as propriedades do DataFrame
pd.set_option('display.max_rows', None)  # Exibir todas as linhas
pd.set_option('display.max_columns', None)  # Exibir todas as colunas
pd.set_option('display.width', 50)  # Largura da tela (para evitar que as colunas sejam truncadas)
pd.set_option('display.expand_frame_repr', True)  # Evitar que as colunas sejam truncadas
pd.set_option('max_colwidth', 20)  # Largura máxima da coluna (para evitar truncamento do conteúdo)

# Função para aplicar cores ao DataFrame
def color_df(val):
    color_map = {
        "Na fila": "red",
        "Orçamento": "orange",
        "Aguardando Peças": "brown",
        "Em serviço": "lightblue",
        "Pronto para retirada": "green"
    }
    color = color_map.get(val, "white")
    return f'background-color: {color}; color: white; font-size: 20px;'

st.set_page_config(
    page_title="Gestão de Pátio de Oficina",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🛠️ Gestão de Pátio de Oficina 🚗")

st.sidebar.image("mecanicar/marca-nova.jpg")
st.sidebar.title("Menu")

choice = st.sidebar.radio("", ["Visualizar Todos os Veículos 📝","Adicionar Veículo 🚙","Visualizar Veículos por Status 📊","Visualizar por Consultor 👨‍🔧", "Visualizar por Mecânico 🔧"])

status_options = ["Na fila", "Orçamento", "Aguardando Peças", "Em serviço", "Pronto para retirada"]

if choice == "Adicionar Veículo 🚙":
    st.subheader("Adicionar Veículo")
    col1, col2, col3 = st.columns(3)

    with col1:
        vehicle = st.text_input("Veículo")

    with col2:
        consultant = st.selectbox("Consultor Responsável", ["Rafael", "Rudimar", "Samuel", "Jéssica", "Paulo"])

    with col3:
        mechanic = st.selectbox("Mecânico Responsável", ["Vini", "Valdo", "Danilo", "Fosco", "Szczhoca", "Weslei"])

    status = st.selectbox("Status", status_options)

    if st.button("Adicionar Veículo"):
        add_vehicle(vehicle, consultant, mechanic, status)
        st.success(f"Veículo \"{vehicle}\" adicionado com sucesso! 🚀")

elif choice == "Visualizar Veículos por Status 📊":
    st.subheader("Visualizar Veículos por Status")

    status_filter = st.selectbox("Selecione um Status", status_options)
    filtered_data = get_data_by_status(status_filter)

    if filtered_data:
        df_filtered = pd.DataFrame(filtered_data, columns=["Veículo", "Consultor", "Mecânico", "Status"])
        st.dataframe(df_filtered.style.map(color_df, subset=["Status"]), use_container_width=True)
    else:
        st.info("Nenhum veículo encontrado com o status selecionado.")        

elif choice == "Visualizar Todos os Veículos 📝":
    st.subheader("Visualizar Todos os Veículos")

    all_data = view_all_data()

    if all_data:
        df_all = pd.DataFrame(all_data, columns=["Veículo", "Consultor", "Mecânico", "Status"])
        
        # Adicionando opções para modificar o consultor e o mecânico
        selected_vehicle = st.selectbox("Selecione um Veículo", df_all["Veículo"].unique())
        current_row = df_all[df_all["Veículo"] == selected_vehicle].iloc[0]  # Obtém a linha correspondente ao veículo selecionado
        current_status = current_row["Status"]
        current_consultant = current_row["Consultor"]
        current_mechanic = current_row["Mecânico"]

        # Define o valor padrão dos selectbox para ser o consultor e o mecânico atuais
        new_consultant = st.selectbox("Selecione um Novo Consultor", ["Paulo", "Jéssica", "Samuel", "Rafael", "Rudimar"], index=["Paulo", "Jéssica", "Samuel", "Rafael", "Rudimar"].index(current_consultant))
        new_mechanic = st.selectbox("Selecione um Novo Mecânico", ["Vini", "Valdo", "Danilo", "Fosco", "Szczhoca", "Weslei"], index=["Vini", "Valdo", "Danilo", "Fosco", "Szczhoca", "Weslei"].index(current_mechanic))
        new_status = st.selectbox("Selecione um Novo Status", status_options, index=status_options.index(current_status))

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Atualizar Consultor, Mecânico e Status"):
                update_vehicle_consultant_mechanic_status(selected_vehicle, new_consultant, new_mechanic, new_status)
                st.success(f"Consultor, Mecânico e Status do veículo \"{selected_vehicle}\" atualizados com sucesso! 🚀")
                st.experimental_rerun()  # Rerun do script para atualizar em tempo real

        with col3:
            delete_button = st.button(f"Excluir {selected_vehicle}")
            if delete_button:
                delete_data(selected_vehicle)
                success_message = st.empty()
                success_message.success(f"Veículo \"{selected_vehicle}\" deletado com sucesso! 🚗")
                success_message_text = success_message.text("")
                time.sleep(2)  # Altere o tempo conforme necessário
                success_message_text.text("Veículo deletado")
                st.experimental_rerun()  # Rerun do script para atualizar em tempo real

        # Renderiza o DataFrame com a coluna de botões
        st.markdown(df_all.style.applymap(color_df, subset=["Status"]).to_html(), unsafe_allow_html=True)

    else:
        st.info("Nenhum veículo encontrado.")

elif choice == "Visualizar por Consultor 👨‍🔧":
    st.subheader("Visualizar Veículos por Consultor")
    consultant = st.selectbox("Selecione um Consultor", ["Paulo", "Jéssica", "Samuel", "Rafael", "Rudimar"])
    data = get_data_by_consultant(consultant)
    if data:
        df = pd.DataFrame(data, columns=["Veículo", "Consultor", "Mecânico", "Status"])
        df_styled = df.style.map(color_df, subset=["Status"]).set_table_styles([{'selector': 'td', 'props': [('font-size', '20px'), ('line-height', '10px')]}])
        st.dataframe(df_styled, use_container_width=True)
    else:
        st.info("Nenhum veículo encontrado para este consultor.")

elif choice == "Visualizar por Mecânico 🔧":
    st.subheader("Visualizar Veículos por Mecânico")
    mechanic = st.selectbox("Selecione um Mecânico", ["Vini", "Valdo", "Danilo", "Fosco", "Szczhoca", "Weslei"])
    data = get_data_by_mechanic(mechanic)
    if data:
        df = pd.DataFrame(data, columns=["Veículo", "Consultor", "Mecânico", "Status"])
        st.dataframe(df.style.map(color_df, subset=["Status"]), use_container_width=True)
    else:
        st.info("Nenhum veículo encontrado para este mecânico.")

st.markdown("<br><hr><center>Desenvolvido por Vinight </center><hr>", unsafe_allow_html=True)
