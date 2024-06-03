# Módulo para criação da tabela ALUNOS
# André Vieira
# 2/6/24

import os
import sys
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from msg.msg_mensagens import Mensagem_Erro

class Criar_Tabela_Alunos():

  def __init__(self):      

    self.msg = Mensagem_Erro()
    self.msg.Origem_Msg(self.__class__.__name__, os.path.basename(__file__))

    self.db_arquivo = "db/banco_de_dados.db"
    self.con = None
    
    self.conectar()
    self.criar_tabela()
    self.encerrar()

  def conectar(self):
    
    try:
      self.con = sqlite3.connect(self.db_arquivo)
    except sqlite3 as erro:
      print("Erro de conexão com banco de dados: ", erro, self.msg) 
    else:
      print("Conexão com banco de dados realizada")

  def criar_tabela(self):

    try:
      with self.con:
        cur = self.con.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS ALUNOS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cpf INTEGER,
                    nome TEXT,
                    email TEXT,
                    telefone TEXT,
                    sexo TEXT,
                    foto TEXT,
                    data_nascimento DATE,
                    turma TEXT,
                    FOREIGN KEY (turma) REFERENCES TURMAS (nome)
                    ON DELETE CASCADE)""")
        print("Tabela ALUNOS criada")
    except sqlite3.Error as erro:
      print ("Erro ao criar tabela ALUNOS: ", erro, self.msg)

  def encerrar(self):
    
    try:
      self.con.close()
    except sqlite3.Error as erro:
      print ("Erro ao tentar fechar o banco de dados", erro, self.msg)
    else:
      print ("Conexão com banco de dados encerrada")