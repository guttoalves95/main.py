from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser


root = Tk()

class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def gerarRelCliente(self):
        self.c = canvas.Canvas('cliente.pdf')

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.RoteadorONU_entry.get()
        self.telefoneRel = self.Mac_entry.get()
        self.cidadeRel = self.Serial_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, "EQUIPAMENTOS")

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700,"Codigo:")
        self.c.drawString(50, 670, "RoteadorONU:")
        self.c.drawString(50, 630, "Mac: ")
        self.c.drawString(50, 600,"Serial:")

        self.c.setFont("Helvetica", 18)
        self.c.drawString(120, 700, self.codigoRel)
        self.c.drawString(200, 670, self.nomeRel)
        self.c.drawString(120, 630, self.telefoneRel)
        self.c.drawString(120, 600, self.cidadeRel)

        self.c.rect(20, 720, 550, 150, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printCliente()


class Funcs():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.RoteadorONU_entry.delete(0, END)
        self.Mac_entry.delete(0, END)
        self.Serial_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect('clientes.bd')
        self.cursor = self.conn.cursor();
        print('Conectando ao banco de dados')

    def desconectar_bd(self):
        self.conn.close();
        print('Desconectando ao banco de dados')

    def montaTabelas(self):
        self.conecta_bd()
        ### criação da tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
                );
        """)
        self.conn.commit();
        print('Banco de dados criado')
        self.desconectar_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.RoteadorONU_entry.get()
        self.telefone = self.Mac_entry.get()
        self.cidade = self.Serial_entry.get()

    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
            VALUES (?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpa_tela()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""SELECT cod, nome_cliente, telefone, cidade FROM clientes 
                ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconectar_bd()

    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.RoteadorONU_entry.insert(END, col2)
            self.Mac_entry.insert(END, col3)
            self.Serial_entry.insert(END, col4)

    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ?""", (self.codigo))
        self.conn.commit()
        self.desconectar_bd()
        self.limpa_tela()
        self.select_lista()

    def alterar_clientes(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""UPDATE clientes SET nome_cliente = ?,telefone = ?, cidade = ?
            WHERE cod = ?""", (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpa_tela()

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Relatorios", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu.add_command(label="Limpa Cliente", command=self.limpa_tela)

        filemenu2.add_command(label="Ficha do cliente", command=self.gerarRelCliente)
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.Mac_entry.insert(END, "%")
        nome = self.Mac_entry.get()
        self.cursor.execute(
            """SELECT cod, nome_cliente, telefone,cidade FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("",END, values=i)
        self.limpa_tela()

        self.desconectar_bd()

class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.botoes_frames1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()

    def tela(self):
        self.root.title('cadastro de clientes')
        self.root.configure(background='teal')
        self.root.geometry('700x500')
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=600)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='snow', highlightbackground='black', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='snow', highlightbackground='black', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def botoes_frames1(self):
        self.canvas_bt = Canvas(self.frame_1, bd=0, bg='darkgrey', highlightbackground= 'gray',
            highlightthickness=3)
        self.canvas_bt.place(relx= 0.19, rely= 0.08, relwidth= 0.22, relheight= 0.19)

        # botão limpar
        self.bt_limpar = Button(self.frame_1, text='Limpar', bd=3, bg='slategray', fg="white",
                                font=('verdana', 8, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.10, relheight=0.15)
        # botao buscar
        self.bt_buscar = Button(self.frame_1, text='Buscar', bd=3, bg='slategray', fg='white',
                                font=('verdana', 8, 'bold'), command= self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        # botao novo
        self.bt_novo = Button(self.frame_1, text='Novo', bd=3, bg='slategray', fg='white', font=('verdana', 8, 'bold'),
                              command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        # botao alterar
        self.bt_alterar = Button(self.frame_1, text='Alterar', bd=3, bg='slategray', fg='white',
                                 font=('verdana', 8, 'bold'), command=self.alterar_clientes)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        # botao apogar
        self.bt_apagar = Button(self.frame_1, text='Apagar', bd=3, bg='slategray', fg='white',
                                font=('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        # criacção da label e entrada do codigo

        self.lb_codigo = Label(self.frame_1, text='Código')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)

        # criação de label e entrada do nome

        self.lb_RoteadorONU = Label(self.frame_1, text='Roteador ONU')
        self.lb_RoteadorONU.place(relx=0.05, rely=0.35)

        self.RoteadorONU_entry = Entry(self.frame_1)
        self.RoteadorONU_entry.place(relx=0.05, rely=0.45, relwidth=0.3)

        # criação da label do Mac

        self.lb_Mac = Label(self.frame_1, text='Mac')
        self.lb_Mac.place(relx=0.05, rely=0.6)

        self.Mac_entry = Entry(self.frame_1)
        self.Mac_entry.place(relx=0.05, rely=0.7, relwidth=0.3)

        # criação label da Serial
        self.lb_Serial = Label(self.frame_1, text='Serial')
        self.lb_Serial.place(relx=0.5, rely=0.6)

        self.Serial_entry = Entry(self.frame_1)
        self.Serial_entry.place(relx=0.5, rely=0.7, relwidth=0.3)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Roteador")
        self.listaCli.heading("#3", text="Mac")
        self.listaCli.heading("#4", text="Serial")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolista.set)
        self.scroolista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)


Application()
