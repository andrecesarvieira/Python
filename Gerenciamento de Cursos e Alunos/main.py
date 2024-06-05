import tkinter as tk

from tkinter import ttk
from tkinter import font
from modulos.janela_principal_criar import JanelaPrincipal
from modulos.tabelas_db_criar import CriarTabelasDB
def main():
  root = tk.Tk()
  JanelaPrincipal(root)
  root.mainloop()

if __name__ == "__main__":
  CriarTabelasDB()
  main()