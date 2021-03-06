#!/usr/local/bin/python3
# Arquivo : rx-sislin.py
# Programa: Solucionador de Sistmas Lineares para o X
# Autor   : Rahul Martim Juliato
# Versão  : 0.1  -  17.04.2018
# Versão  : 0.2  -  02.08.2019 - Suporte ao MacOS
# Versão  : 0.3  -  29.12.2019 - Mudança de nome para rx-sislin (antigo rSisLinx)

# For future implementation
# ⎨ ⎧ ⎩ ⎪

#---===[0. Bibliotecas]===---
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk
import math
import numpy as np
#---===[0. Fim das Bibliotecas]===---


#---===[0.5 Variáveis Globais]===---
tamanho_A = 2
modoeng = False
#---===[0.5 Fim das Variáveis Globais]===---


#---===[1. Funções]===---
def quit():
    """ Sai do programa destruindo o necessário
    """
    global janela
    janela.destroy()

def engenharia():
    """ Seta/Reseta o modo engenharia das respostas
    """
    global modoeng
    if modoeng is True:
        modoeng = False
    else:
        modoeng = True

def sobre():
    """ Mostra as informações do programa
    """
    mb.showinfo("rx-sislin",'''

rx-sislin
Solucionador de Sistemas Lineares

Versão: 0.3

Autor : Rahul Martim Juliato
E-mail: rahul.juliato@gmail.com
URL   : www.rahuljuliato.com

''')


def erro(mensagem):
    """Sobre uma messagebox de erro com a mensagem
    passada"""
    mb.showerror("Erro!", mensagem)

    
    
# Snipet para conversão em números de engenharia
from math import floor, log10

def powerise10(x):
    """ Returns x as a*10**b with 0 <= a < 10
    """
    if x == 0: return 0,0
    Neg = x < 0
    if Neg: x = -x
    a = 1.0 * x / 10**(floor(log10(x)))
    b = int(floor(log10(x)))
    if Neg: a = -a
    return a,b

def eng(x):
    """Return a string representing x in an engineer friendly notation"""
    a,b = powerise10(x)
    if -3 < b < 3: return "%.4g" % x
    a = a * 10**(b % 3)
    b = b - b % 3
    return "%.4gE%s" % (a,b)
## Fim do Snipet


def geramatriz(col, lin, jan="janela"):
    """ Gera a matriz de variáveis do sistema
    """
    colunas = range(0, col)
    linhas  = range(0, lin)

    global entradas, label
    entradas = {}
    label = {}
    
    i  = 0
    ii = 0

    
    for y in linhas:
        letrinhas = chr(ord("a"))
        
        i = 0      
        for x in colunas:
            e = tk.Entry(janela)
            e.configure(width = 10)
            e.grid(sticky='E', row = ii, column = i)
            entradas[str('%s%s' % (str(x), str(y)))] = e

            i += 1
            if x == col-1:
                sinal = letrinhas+'   = '
            else:
                sinal = letrinhas+' +'

            letrinhas = chr(ord(letrinhas)+1)
            
            lb = tk.Label(janela, text=sinal)
            lb.grid(row=ii, column=i)
            label[str('%s%s' % (str(x), str(y)))] = lb

            i += 1

        ii += 1


def geravetor(col, jan="janela"):
    """ Gera o vetor de soluções do sistema
    """
    colunas = range(0, col)

    global saidas
    saidas = {}
    
    i = 0      
    for x in colunas:
        e = tk.Entry(janela)
        e.configure(width = 10)
        e.grid(sticky='W', row = i, column = col*2)
        saidas[str('%s' % (str(x)))] = e
        i += 1
        

def calcula(col, lin):
    """ Calcula a solução para as variáveis do sistema
    """
    global modoeng
    
    linhas  = range(0, lin)
    colunas = range(0, col)

    resposta = ""
    imprimir = ""

    A = [ [ None for y in range( col ) ] for x in range( lin ) ]

    B = [ None for y in range( col ) ]

    resultado = [ None for y in range( col ) ]

    i  = 0

    for y in linhas:

        B[y] = float(saidas[str('%s' % (str(y)))].get())
        
        i = 0      
        for x in colunas:
            A[y][x] = float(entradas[str('%s%s' % (str(x), str(y)))].get())
            i += 1
        
    print(A)
    print(B)

    try:
        resultado = np.dot(np.linalg.inv(np.matrix(A)), B)

        resposta = str(resultado)
        resposta = resposta.strip('[]').split()

        for x in range(0,len(resposta)):
            if modoeng is True:
                imprimir = imprimir + chr(ord("a")+x) + '=' + str("%s" %(str(eng(float(resposta[x])))))+ " "
            else:
                imprimir = imprimir + chr(ord("a")+x) + '=' + str("%s" %(resposta[x]))+ " "
                
        ent_resposta.delete(0, 10000)
        ent_resposta.insert(0,imprimir)
        
    except np.linalg.linalg.LinAlgError:
        erro("Esse sistema não tem solução única!")


def aumenta():
    """ Aumenta a matriz
    """
    global tamanho_A
    destroi(tamanho_A, tamanho_A)

    if tamanho_A < 10:
        tamanho_A = tamanho_A + 1

    else:
        erro("Limite excedido")
    gera()
    pass


def diminui():
    """ Diminui a matriz
    """
    global tamanho_A
    destroi(tamanho_A, tamanho_A)

    if tamanho_A > 1:
        tamanho_A = tamanho_A - 1

    gera()
    pass


def gera():
    """ Gera os widgets da tela principal
    """
    geramatriz(tamanho_A, tamanho_A)
    geravetor(tamanho_A)
    parteinferior()

    
def parteinferior():
    """ Gera/Atualiza a parte inferior da janela
    """
    separador.grid(sticky = 'EW', pady = 10, columnspan = tamanho_A * 3 , row = tamanho_A + 1)
    lab_resposta.grid(sticky = 'W', row = tamanho_A + 2, column = 0)
    ent_resposta.grid(sticky = 'EW', row = tamanho_A + 3, columnspan = tamanho_A * 3)
    bot_mais.grid(sticky = 'EW', row = tamanho_A + 4, column=0)
    bot_menos.grid(sticky = 'EW', row = tamanho_A + 4, column=2)
    bot_calcula.grid(sticky = 'EW', row = tamanho_A + 5, columnspan = 3)
    chk_eng.grid(sticky = 'W', row = tamanho_A + 6)
    

    
def destroi(col, lin):
    """ Destrói todos os labels e entries
    """
    colunas = range(0, col)
    linhas  = range(0, lin)
    
    i  = 0
    ii = 0
    
    for y in linhas:
        i = 0
        saidas[str('%s' % (str(y)))].destroy()
        for x in colunas:
            entradas[str('%s%s' % (str(x), str(y)))].destroy()
            label[str('%s%s' % (str(x), str(y)))].destroy()
            i += 1
        ii += 1
#---===[1. Fim das Funções]===---



#---===[2. Início da geração da Janela]===---
# 2.0. Definições principais da janela
janela = tk.Tk()
#janela.geometry("500x200")
janela.wm_title('rx-sislin v0.3')
janela.wm_minsize(380,220)
janela.grid_anchor(anchor='c')
#janela.tk_setPalette('gray')


# 2.0. Barra de menu
barramenu = tk.Menu(janela)
arquivo = tk.Menu(barramenu, tearoff=800)
arquivo.add_command(label="Sobre", command=sobre)
arquivo.add_separator()
arquivo.add_command(label="Sair", command=quit)
barramenu.add_cascade(label="Sistema Linear:", menu=arquivo)

barramenu.add_separator()
barramenu.add_command(label="--[+]--", command= lambda: aumenta())

barramenu.add_command(label="--[-]--", command= lambda: diminui())

barramenu.add_command(label="--[Calcular]--", command= lambda: calcula(tamanho_A,tamanho_A))

barramenu.add_checkbutton(label="ENG", command=engenharia)
                    
janela.config(menu=barramenu)

# 2.0 Título dentro da janela principal
#titulo = tk.Label(janela, text="r[Sistemas Lineares]X", font="Arial 16 bold", height=2)
#titulo.grid(column = 0, row = 0, sticky="NSEW")


geramatriz(tamanho_A, tamanho_A)
geravetor(tamanho_A)


separador = tk.ttk.Separator()
ent_resposta = tk.Entry(janela)
lab_resposta = tk.Label(janela, text="Soluções: ")
bot_mais = tk.Button(janela, text="+", command=aumenta)
bot_menos = tk.Button(janela, text="-", command=diminui)
bot_calcula = tk.Button(janela, text="Calcular", command=  lambda: calcula(tamanho_A,tamanho_A))
chk_eng = tk.Checkbutton(janela, text="ENG", command=engenharia)
parteinferior()


tk.mainloop()
#---===[2 Fim da Geração da Janela]===---
