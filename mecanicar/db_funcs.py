import sqlite3

def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY,
                vehicle TEXT NOT NULL,
                consultant TEXT NOT NULL,
                mechanic TEXT NOT NULL,
                status TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()
    
# Função para adicionar um veículo ao banco de dados
def add_vehicle(vehicle, consultant, mechanic, status):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO vehicles (vehicle, consultant, mechanic, status) VALUES (?, ?, ?, ?)', (vehicle, consultant, mechanic, status))
    conn.commit()
    conn.close()

# Função para atualizar o status do veículo
def update_vehicle_status(vehicle, new_status):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE vehicles SET status=? WHERE vehicle=?', (new_status, vehicle))
    conn.commit()
    conn.close()

# Função para visualizar todos os veículos
def view_all_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT vehicle, consultant, mechanic, status FROM vehicles')
    data = c.fetchall()
    conn.close()
    return data

# Função para visualizar veículos por status
def get_data_by_status(status):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT vehicle, consultant, mechanic, status FROM vehicles WHERE status=?', (status,))
    data = c.fetchall()
    conn.close()
    return data

# Função para visualizar veículos por consultor
def get_data_by_consultant(consultant):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT vehicle, consultant, mechanic, status FROM vehicles WHERE consultant=?', (consultant,))
    data = c.fetchall()
    conn.close()
    return data

# Função para visualizar veículos por mecânico
def get_data_by_mechanic(mechanic):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT vehicle, consultant, mechanic, status FROM vehicles WHERE mechanic=?', (mechanic,))
    data = c.fetchall()
    conn.close()
    return data

def delete_data(vehicle):
    """Exclui um veículo da tabela 'vehicles' com base no nome do veículo."""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM vehicles WHERE vehicle=?', (vehicle,))
    conn.commit()
    conn.close()
    
def create_table():
    """Cria a tabela 'vehicles' no banco de dados."""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY,
                vehicle TEXT NOT NULL,
                consultant TEXT NOT NULL,
                mechanic TEXT NOT NULL,
                status TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def update_vehicle_consultant_mechanic_status(vehicle, new_consultant, new_mechanic, new_status):
    """Atualiza o consultor, o mecânico e o status de um veículo na tabela 'vehicles'."""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE vehicles SET consultant=?, mechanic=?, status=? WHERE vehicle=?', (new_consultant, new_mechanic, new_status, vehicle))
    conn.commit()
    conn.close()