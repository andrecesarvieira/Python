# Objetivo: Criação das tabelas do banco de dados
# Autor...: André Vieira
# Data....: 3/6/24

import os
import sys
from modulos.db.conexao import ConectarBancodeDados
from modulos.db.tabela_alunos import CriarTabelaAlunos
from modulos.db.tabela_cursos import CriarTabelaCursos
from modulos.db.tabela_turmas import CriarTabelaTurmas

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class CriarTabelasDB():
  def conectar():
    c = ConectarBancodeDados()
    conexao = c.conectar()
    
    if conexao:
      alunos = CriarTabelaAlunos()
      cursos = CriarTabelaCursos()
      turmas = CriarTabelaTurmas()
      alunos.criar(conexao)
      cursos.criar(conexao)
      turmas.criar(conexao)
      c.encerrar(conexao)
    else:
      print("Não foi possível criar as tabelas do banco de dados.")