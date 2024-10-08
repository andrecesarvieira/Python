import re
import tkinter as tk
from tkinter import ttk
import sv_ttk

class appCalcGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Área COBOL")
        self.root.resizable(False, False)
        self.criarWidgets()

    def criarWidgets(self):
        self.criarAreaTexto()
        #self.criarBotoes()
        #self.criarLabelResultado()
        #self.criarArvoreCampos()

    def criarAreaTexto(self):
        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.area_texto = tk.Text(self.frame, bd=1, relief='groove', wrap="none")

        vsb = ttk.Scrollbar(self.frame, command=self.area_texto.yview, orient="vertical")
        vsb.grid(row=0, column=1, sticky="ns")

        self.area_texto.configure(yscrollcommand=vsb.set, xscrollcommand=False)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
       
        self.area_texto.grid(row=0, column=0, sticky="nsew")

    def criarBotoes(self):
        self.frame_botoes = ttk.Frame(self.root)
        self.frame_botoes.grid(row=1, column=0, columnspan=2, pady=5)
        self.botao_calcular = ttk.Button(
            self.frame_botoes, text="Calcular Área", command=self.calcularArea)
        self.botao_calcular.grid(row=0, column=0, padx=5)
        self.botao_limpar = ttk.Button(
            self.frame_botoes, text="Limpar", command=self.limparAreaTexto)
        self.botao_limpar.grid(row=0, column=1, padx=5)
        self.botao_tema = ttk.Button(
            self.frame_botoes, text="Tema", command=self.mudarTema)
        self.botao_tema.grid(row=0, column=2, padx=5)

    def criarLabelResultado(self):
        self.label_resultado = ttk.Label(
            self.root, text="", font=("Helvetica", 10, "bold"))
        self.label_resultado.grid(row=2, column=0, columnspan=2, pady=5)

    def criarArvoreCampos(self):
        self.frame_arvore = ttk.Frame(self.root)
        self.frame_arvore.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.arvore = ttk.Treeview(self.frame_arvore, columns=(
            'Nome', 'Tipo', 'Tamanho', 'Ocorrências'), show='headings')
        self.arvore.heading('Nome', text='Nome do Campo')
        self.arvore.heading('Tipo', text='Tipo')
        self.arvore.heading('Tamanho', text='Tamanho')
        self.arvore.heading('Ocorrências', text='Ocorrências')
        self.barra_rolagem = ttk.Scrollbar(
            self.frame_arvore, orient="vertical", command=self.arvore.yview)
        self.arvore.configure(yscrollcommand=self.barra_rolagem.set)
        self.arvore.grid(row=0, column=0, sticky="nsew")
        self.barra_rolagem.grid(row=0, column=1, sticky="ns")
        self.frame_arvore.grid_rowconfigure(0, weight=1)
        self.frame_arvore.grid_columnconfigure(0, weight=1)

    def calcularArea(self):
        area_cobol = self.area_texto.get(1.0, tk.END)
        area_total, campos = Calculo.calcularAreaTotal(area_cobol)
        self.label_resultado.config(text=f"Área total do layout: {area_total} bytes")
        self.exibirCampos(campos)

    def limparAreaTexto(self):
        self.area_texto.delete(1.0, tk.END)
        self.arvore.delete(*self.arvore.get_children())

    def exibirCampos(self, campos):
        self.arvore.delete(*self.arvore.get_children())
        for campo in campos:
            self.arvore.insert('', 'end', values=campo)
            print(campo)

    def mudarTema(self):
        sv_ttk.toggle_theme()

class Calculo:
    @staticmethod
    def calcularAreaTotal(area_cobol):
        total_area = 0
        campos = []
        linhas = area_cobol.split('\n')
        redefinidos = set()
        redefinindo = False
        nivel_redefine = 0
        fatores_ocorrencia = [1] * 50  # Lista inicializada para 50 níveis de hierarquia

        for linha in linhas:
            match_redefine = re.match(r'\s*(\d+)\s+(\S+)\s+REDEFINES\s+(\S+)\.', linha)
            if match_redefine:
                redefinidos.add(match_redefine.group(3))
                redefinindo = True
                nivel_redefine = int(match_redefine.group(1))
                continue

            if redefinindo:
                match_nivel = re.match(r'\s*(\d+)', linha)
                if match_nivel:
                    nivel_linha = int(match_nivel.group(1))
                    if nivel_linha <= nivel_redefine:
                        redefinindo = False
                    else:
                        continue

            expressao = (
                r'\s*(\d+)\s+(\S+)\s+PIC\s+([9XZS])'
                r'(?:\((\d+)\))?'
                r'(?:V9\((\d+)\))?'  # Captura campos com ponto decimal
                r'(?:\s+OCCURS\s+(\d+))?' # Captura ocorrências
                r'(?:\s+(BINARY|COMP(?:-1|-2|-3|-4|-5)?))?'
            )
            
            match_campo = re.match(expressao, linha)
            if match_campo:
                nivel = int(match_campo.group(1))
                nome = match_campo.group(2)
                tipo = match_campo.group(3)
                tamanho = int(match_campo.group(4)) if match_campo.group(4) else 1
                decimal_size = int(match_campo.group(5)) if match_campo.group(5) else 0
                ocorrencias = int(match_campo.group(6)) if match_campo.group(6) else 1
                comp_tipo = match_campo.group(7)

                if tipo in ['9', 'S']:
                    tamanho += decimal_size

                if comp_tipo:
                    if comp_tipo in ['BINARY', 'COMP', 'COMP-4']:
                        if tamanho <= 4:
                            tamanho = 2
                        elif tamanho <= 9:
                            tamanho = 4
                        elif tamanho <= 18:
                            tamanho = 8
                    elif comp_tipo == 'COMP-1':
                        tamanho = 4
                    elif comp_tipo == 'COMP-2':
                        tamanho = 8
                    elif comp_tipo == 'COMP-3':
                        tamanho = (tamanho + 1) // 2
                    elif comp_tipo == 'COMP-5':
                        if tamanho <= 4:
                            tamanho = 2
                        elif tamanho <= 9:
                            tamanho = 4
                        elif tamanho <= 18:
                            tamanho = 8

                fatores_ocorrencia[nivel] = ocorrencias

                if nome in redefinidos:
                    continue

                multiplicador = 1
                for i in range(1, nivel + 1):
                    multiplicador *= fatores_ocorrencia[i]

                total_area += tamanho * multiplicador
                campos.append((nome, tipo, tamanho, multiplicador))

        return total_area, campos

def main():
    root = tk.Tk()
    appCalcGUI(root)
    sv_ttk.use_light_theme()
    root.mainloop()

if __name__ == "__main__":
    main()
