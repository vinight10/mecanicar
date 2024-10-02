import streamlit as st
import pandas as pd
import sqlite3 
from db_funcs import *
from PIL import Image
import time
import os
import shutil
from datetime import datetime, timedelta
import bcrypt  # Para hashing de senhas

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
    return f'background-color: {color_map.get(val, "white")};'

# Função para verificar as credenciais do usuário com hash de senha
USER_DATA = {
    "vini": bcrypt.hashpw("senha123".encode(), bcrypt.gensalt()),
    "jessica": bcrypt.hashpw("senha456".encode(), bcrypt.gensalt()),
    "paulo": bcrypt.hashpw("senha0122".encode(), bcrypt.gensalt()),
    "rafa": bcrypt.hashpw("senha123".encode(), bcrypt.gensalt()),
    "rudi": bcrypt.hashpw("senha222".encode(), bcrypt.gensalt()),
    "samu": bcrypt.hashpw("senha77".encode(), bcrypt.gensalt()),
    "danilo": bcrypt.hashpw("senha55".encode(), bcrypt.gensalt()),
    "fosco": bcrypt.hashpw("senha11".encode(), bcrypt.gensalt()),
    "weslei": bcrypt.hashpw("senha22".encode(), bcrypt.gensalt()),
    "szcz": bcrypt.hashpw("senha44".encode(), bcrypt.gensalt())
}

def authenticate(username, password):
    hashed_pw = USER_DATA.get(username)
    if hashed_pw and bcrypt.checkpw(password.encode(), hashed_pw):
        return True
    return False

# Função principal
def main():
    st.title("🛠️ Gestão de Pátio de Oficina 🚗")
    
    # Verifica se o usuário está autenticado
    if not is_authenticated():
        show_login_page()
        st.empty()  # Limpar a página
    else:
        show_main_page()

# Função para verificar se o usuário está autenticado
def is_authenticated():
    return st.session_state.get("authenticated", False)

# Função para exibir a página de login
def show_login_page():
    try:
        image = Image.open("mecanicar/marca-nova.jpg")
        st.image(image)
    except FileNotFoundError:
        st.error("Imagem não encontrada.")
        
    st.title("Página de Login")
    username = st.text_input("Nome de Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.success("Login bem-sucedido!")
            set_session_data(username, password)  # Definir a sessão
            show_main_page()  # Redirecionar para a página principal após o login
        else:
            st.error("Nome de usuário ou senha incorretos.")

# Função para definir os dados da sessão após o login
def set_session_data(username, password):
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.password = password
    set_session_cookie()  # Definir o cookie de sessão

# Função para definir o cookie de sessão
def set_session_cookie():
    expiration_time = datetime.now() + timedelta(minutes=30)
    expiration_timestamp = expiration_time.timestamp()
    session_cookie = {
        "username": st.session_state.username, 
        "password": st.session_state.password, 
        "max_age": expiration_timestamp
    }
    st.experimental_set_query_params(**session_cookie)

# Função para exibir a página principal
def show_main_page():
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

        if not filtered_data.empty:
            df_filtered = pd.DataFrame(filtered_data, columns=["Veículo", "Consultor", "Mecânico", "Status"])
            st.dataframe(df_filtered.style.applymap(color_df, subset=["Status"]))
        else:
            st.info("Nenhum veículo encontrado com o status selecionado.")        

    elif choice == "Visualizar Todos os Veículos 📝":
        st.subheader("Visualizar Todos os Veículos")

        all_data = view_all_data()

        if not all_data.empty:
            df_all = pd.DataFrame(all_data, columns=["Veículo", "Consultor", "Mecânico", "Status"])

            selected_vehicle = st.selectbox("Selecione um Veículo", df_all["Veículo"].unique())
            current_row = df_all[df_all["Veículo"] == selected_vehicle].iloc[0]
            current_status = current_row["Status"]
            current_consultant = current_row["Consultor"]
            current_mechanic = current_row["Mecânico"]

            new_consultant = st.selectbox("Selecione um Novo Consultor", ["Paulo", "Jéssica", "Samuel", "Rafael", "Rudimar"], index=["Paulo", "Jéssica", "Samuel", "Rafael", "Rudimar"].index(current_consultant))
            new_mechanic = st.selectbox("Selecione um Novo Mecânico", ["Vini", "Valdo", "Danilo", "Fosco", "Szczhoca", "Weslei"], index=["Vini", "Valdo", "Danilo", "Fosco", "Szczhoca", "Weslei"].index(current_mechanic))
            new_status = st.selectbox("Selecione um Novo Status", status_options, index=status_options.index(current_status))

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("Atualizar Consultor, Mecânico e Status"):
                    update_vehicle_consultant_mechanic_status(selected_vehicle, new_consultant, new_mechanic, new_status)
                    st.success(f"Consultor, Mecânico e Status do veículo \"{selected_vehicle}\" atualizados com sucesso! 🚀")

            with col3:
                delete_button = st.button(f"Excluir {selected_vehicle}")
                if delete_button:
                    delete_data(selected_vehicle)
                    success_message = st.empty()
                    success_message.success(f"Veículo \"{selected_vehicle}\" deletado com sucesso! 🚗")
                    time.sleep(2)
                    st.experimental_rerun()
            
            st.dataframe(df_all.style.applymap(color_df, subset=["Status"]))
        else:
            st.info("Nenhum veículo encontrado.")

    elif choice == "Visualizar por Consultor 👨‍🔧":
        st.subheader("Visualizar Veículos por Consultor")
        consultant = st.selectbox("Selecione um Consultor", ["Paulo", "Jéssica", "Samuel", "Rafael", "Rudimar"])
        data = get_data_by_consultant(consultant)
        if not data.empty:
            df = pd.DataFrame(data, columns=["Veículo", "Consultor", "Mecânico", "Status"])
            st.dataframe(df.style.applymap(color_df, subset=["Status"]))
        else:
            st.info(f"Nenhum veículo encontrado para o consultor {consultant}.")

    elif choice == "Visualizar por Mecânico 🔧":
        st.subheader("Visualizar Veículos por Mecânico")
        mechanic = st.selectbox("Selecione um Mecânico", ["Vini", "Valdo", "Danilo", "Fosco", "Szczhoca", "Weslei"])
        data = get_data_by_mechanic(mechanic)
        if not data.empty:
            df = pd.DataFrame(data, columns=["Veículo", "Consultor", "Mecânico", "Status"])
            st.dataframe(df.style.applymap(color_df, subset=["Status"]))
        else:
            st.info(f"Nenhum veículo encontrado para o mecânico {mechanic}.")

# Função principal
if __name__ == '__main__':
    main()
