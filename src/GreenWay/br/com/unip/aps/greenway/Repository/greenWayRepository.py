import sqlite3
from typing import List, Dict, Optional
import os

class GreenWayRepository:
    def __init__(self):
        data_dir = os.path.join(os.path.dirname(__file__), '../../../../../../resources', 'dataBase')
        os.makedirs(data_dir, exist_ok=True)
        self.db_path = os.path.join(data_dir, 'greenway.db')
        print(f"Database path set to: {self.db_path}")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            self._create_tables(cursor)
            if self._count_users(cursor) == 0:
                self._initialize_default_users(cursor)
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self, cursor):
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nickName TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            kg INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0,
            missao INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

    def _initialize_default_users(self, cursor):
        default_users = [
            ("Ana Silva", "anagreen", "ana.silva@email.com", "Eco2025#", 12, 850, 12),
            ("Pedro Santos", "pedroearth", "pedro.santos@email.com", "Terra2025!", 20, 720, 12),
            ("Mariana Costa", "marieco", "mari.costa@email.com", "Planet2025@", 27, 930, 12),
            ("Lucas Oliveira", "lucasgreen", "lucas.oli@email.com", "Nature2025#", 17, 650, 12),
            ("Julia Martins", "jurecycle", "ju.martins@email.com", "Recycle2025!", 33, 880, 12),
            ("Gabriel Souza", "gabisustain", "gabi.souza@email.com", "Clean2025@", 22, 790, 12),
            ("Beatriz Lima", "biaearth", "bia.lima@email.com", "Earth2025#", 6, 920, 12),
            ("Rafael Mendes", "rafaeco", "rafa.mendes@email.com", "Green2025!", 7, 840, 12),
            ("Carolina Ferreira", "carolplanet", "carol.ferreira@email.com", "Save2025@", 1, 750, 12),
            ("Thiago Almeida", "thienvironment", "thiago.almeida@email.com", "Future2025#", 9, 890, 12)
        ]
        
        cursor.executemany('''
        INSERT INTO users (nome, nickName, email, senha, kg, score, missao)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', default_users)

    def _count_users(self, cursor) -> int:
        cursor.execute('SELECT COUNT(*) FROM users')
        return cursor.fetchone()[0]
        
    def count_users(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            return self._count_users(cursor)

    def get_all_users(self) -> List[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nome, nickName, email, senha, score, kg, missao FROM users')
            users = []
            for row in cursor.fetchall():
                users.append({
                    'nome': row[0],
                    'nickName': row[1],
                    'email': row[2],
                    'senha': row[3],
                    'kg': row[4],
                    'score': row[5],
                    'missao': row[6]
                })
            return users

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT nome, nickName, email, senha, kg, score, missao
            FROM users WHERE email = ?
            ''', (email,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'nome': row[0],
                    'nickName': row[1],
                    'email': row[2],
                    'senha': row[3],
                    'kg': row[4],
                    'score': row[5],
                    'missao': row[6]
                }
            return None

    def get_user_by_nickname(self, nickname: str) -> Optional[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT nome, nickName, email, senha, kg, score, missao
            FROM users WHERE nickName = ?
            ''', (nickname,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'nome': row[0],
                    'nickName': row[1],
                    'email': row[2],
                    'senha': row[3],
                    'kg': row[4],
                    'score': row[5],
                    'missao': row[6]
                }
            return None
        
    def get_user_ranking_position(self, user_email: str) -> Optional[int]:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
            
                cursor.execute('''
                WITH ranked_users AS (
                    SELECT 
                        email,
                        score,
                        ROW_NUMBER() OVER (ORDER BY score DESC) as position
                    FROM users
                )
                SELECT position 
                FROM ranked_users 
                WHERE email = ?
                ''', (user_email,))
            
                result = cursor.fetchone()
            
                if result:
                    position = result[0]
                    return position
                else:
                    print(f"Usuário {user_email} não encontrado no ranking")
                    return None
                
        except sqlite3.Error as e:
            print(f"Erro ao buscar posição no ranking: {e}")
            return None

    def authenticate_user(self, email: str, senha: str) -> Optional[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT nome, nickName, email, senha, kg, score, missao
            FROM users WHERE email = ? AND senha = ?
            ''', (email, senha))
        
            row = cursor.fetchone()
            if row:
                return {
                    'nome': row[0],
                    'nickName': row[1],
                    'email': row[2],
                    'senha': row[3],
                    'kg': row[4],
                    'score': row[5],
                    'missao': row[6]
                }
            return None

    def create_user(self, user: Dict) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO users (nome, nickName, email, senha, kg, score, missao)
                VALUES (?, ?, ?, ?, ?, ?, ?) 
                ''', (
                    user['nome'], 
                    user['nickName'], 
                    user['email'], 
                    user['senha'], 
                    user.get('kg', 0), 
                    user.get('score', 0),
                    user.get('missao', 0) 
                ))
                conn.commit() 
                print(f" USUÁRIO CRIADO | Nome: {user['nome']} | Apelido: {user['nickName']} | Email: {user['email']} | Senha: {'*' * len(user['senha'])} | KG: {user.get('kg', 0)} | Score: {user.get('score', 0)} | Missao: {user.get('missao', 0)} | ID: {cursor.lastrowid}")
                return True
        except sqlite3.IntegrityError as e:
            print(f"Erro de integridade (email/nickname duplicado): {e}")
            return False
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return False

    def update_user_score(self, email: str, new_score: int) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                UPDATE users SET score = ? WHERE email = ?
                ''', (new_score, email))
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def delete_user(self, email: str) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM users WHERE email = ?', (email,))
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False
