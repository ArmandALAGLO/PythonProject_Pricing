# Voici la contruction de notre priceur pour les options Européennes utilisant la méthode de Monte Carlo

from math import *
from numpy import *
from scipy.stats import norm
from tkinter import *
from tkinter import messagebox
from random import gauss

def lecture_donnee():
    global Prix_Option;
    callput = valeur.get()
    S = float(Stock_Entree.get()) 
    K = float(Strike_Entree.get())
    time = float(Maturite_Entree.get())
    risk_free_rate = float(Risk_Entree.get())
    sigma = float(Volatilite_Entree.get()) 
    
    if callput == 1:
            Prix_Option = call_price (ListePayoffs, stock_price, call_payoff, escompte)
            Text_Option = 'Prix option Call Européen: '
    else:
            Prix_Option = put_price (ListePayoffs, stock_price, call_payoff, escompte)
            Text_Option = 'Prix option Put Européen: '
 
    T.delete(0.0, 'end')
    T.insert(END, Text_Option)
    T.insert(END, "%0.2f" % Prix_Option)   
    return

#Définition de la fonction qui retourne des valeurs aléatoires du stock
def stock_price(S,risk_free_rate, sigma, time):
    v = float(sigma.get())
    T = float(time.get())
    Sp = float(S.get())
    r = float(risk_free_rate.get())
    stockp = Sp * exp((r - 0.5 * v**2) * T + v * sqrt(T) * gauss(0,1.0))
    return stockp

# Fonctions qui retournent la valeur du payoff du call et du put 
def call_payoff(ST,K):
    kk = float(K.get())
    payoffc  =max(0.0,ST-kk)
    return payoffc

def put_payoff(ST,K):
    kk = float(K.get())    
    payoffp  =max(0.0,kk-ST)
    return payoffp

#Calcul du facteur de escompte pour actualiser les valeurs
def escompte (risk_free_rate, time):
    T = float(time.get())
    r = float(risk_free_rate.get())
    esc = exp(-r * T)
    return esc
        
# Définition des fonctions qui donnent le prix de l'option call ou put en utilisant la moyenne de 10000 stocks trouvés avec la fonction "stock price"

ListePayoffs = []

def call_price (ListePayoffs, stock_price, call_payoff, escompte):
        for i in range(2000):
            ST = stock_price(S,risk_free_rate, sigma, time)
            ListePayoffs.append(call_payoff(ST, K))
        callp = escompte(risk_free_rate, time) * (sum(ListePayoffs) / float(len(ListePayoffs)))
        ListePayoffs[:] = [] # cela permet de reinitialiser ma liste 
        return callp
        
def put_price (ListePayoffs, stock_price, call_payoff, escompte):
        for i in range(2000):
            ST = stock_price(S,risk_free_rate, sigma, time)
            ListePayoffs.append(put_payoff(ST, K))
        putp = escompte(risk_free_rate, time) * (sum(ListePayoffs) / float(len(ListePayoffs)))
        ListePayoffs[:] = []
        return putp

# Création de objet fenêtre tkinter pour MC ainsi que la définition de ses propriétés

fenetre_MC = Tk()

S = StringVar(); 
K = StringVar(); 
time = StringVar(); 
risk_free_rate = StringVar(); 
sigma = StringVar()

fenetre_MC.title("Options Européennes Calculées avec Monte Carlo") 
fenetre_MC.geometry("450x410+150+125")  
lbl = Label(fenetre_MC, text = "Call et Put Options Européennes:",).pack(anchor=W)

valeur = IntVar() 
Radiobutton(fenetre_MC, text="Call Européen avec MC", padx = 40, pady = 15, variable=valeur, value=1).pack(anchor=W)
Radiobutton(fenetre_MC, text="Put Européen avec MC", padx = 40, variable=valeur, value=2).pack(anchor=W)

Label_Position = { 'S' : [8, 130], 'K' : [8, 160], 'Maturity' :[8, 190], 'Risk' :[8, 220], 'Vol' :[8, 250]}
BtnPosX = 190

S_label = Label(fenetre_MC, text = "S (prix sous-jacent): ")
S_label.place(x=Label_Position['S'][0], y=Label_Position['S'][1])
K_label = Label(fenetre_MC, text = "K (K price ou prix exercé): ")
K_label.place(x=Label_Position['K'][0], y=Label_Position['K'][1])
Maturity_label = Label(fenetre_MC, text = "T (Maturité) en années: ")
Maturity_label.place(x=Label_Position['Maturity'][0], y=Label_Position['Maturity'][1])
Risk_label = Label(fenetre_MC, text = "r (Risk-free rate) en décimales: ")
Risk_label.place(x=Label_Position['Risk'][0], y=Label_Position['Risk'][1])
Volatility_Label = Label(fenetre_MC, text = "V (Volatilité): ")
Volatility_Label.place(x=Label_Position['Vol'][0], y=Label_Position['Vol'][1])
Stock_Entree = Entry(textvariable=S)
Stock_Entree.place(x=BtnPosX, y=Label_Position['S'][1])
Strike_Entree = Entry(textvariable=K)
Strike_Entree.place(x=BtnPosX, y=Label_Position['K'][1])
Maturite_Entree = Entry(textvariable=time)
Maturite_Entree.place(x=BtnPosX, y=Label_Position['Maturity'][1])
Risk_Entree = Entry(textvariable=risk_free_rate)
Risk_Entree.place(x=BtnPosX, y=Label_Position['Risk'][1])
Volatilite_Entree = Entry(textvariable=sigma)
Volatilite_Entree.place(x=BtnPosX, y=Label_Position['Vol'][1])
 
bouton_calculer = Button(fenetre_MC, text = "Cliquer pour donner le prix : ",command = lecture_donnee)
bouton_calculer.place(x=5, y=305)
bouton_calculer.config(width=23, height=1)

T = Text(fenetre_MC, height=3, width=32)
T.place(x=180, y=305)
 
fenetre_MC.mainloop()