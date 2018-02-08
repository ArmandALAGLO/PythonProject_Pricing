# Voici la contruction de notre priceur incluant le modèle de Black&Scholes pour les options Européennes et la méthode Binomiale pour les options Américaines

from math import * # appel de toutes les méthodes de l'objet math
from numpy import *
from scipy.stats import norm # appel à la méthode norm qui nous permet d'avoir access à la fonction de densité de probabilité pdf et sa fonction de distribution cumulée cdf associée
from tkinter import * # appel de toutes les méthodes de l'objet tkinter
from tkinter import messagebox
from random import gauss

# Lecture des datas et calcul des outputs - fonction principale avec appel des fonctions définies plus bas
def lecture_donnee():
    global d1; global d2; global Prix_Option; global N;
    callput = valeur.get() # ┤permet de lire la valeur qui indique s'il s'agit d'un call ou un put
    S = float(Stock_Entree.get()) # la méthode get() permet de lire les données saisies par la méthode entry() 
    K = float(Strike_Entree.get())
    time = float(Maturite_Entree.get())
    risk_free_rate = float(Risk_Entree.get())
    sigma = float(Volatilite_Entree.get())
    N=2000 

    d1 = ((log(S / K) + (risk_free_rate + 0.5 * sigma *sigma) * time) / (sigma * sqrt (time)))
    d2 = d1 - sigma * sqrt(time)   
    
    if callput == 1: # ceci identifie la valeur de la variable "valeur" (par exemple ici = 1) en cliquant sur le radioboutton call_BlackScholes
        Prix_Option = call_option_européenne(S, K, time, risk_free_rate, sigma)
        Text_Option = 'Prix option Call Européen: '
        delta = delta_call_option_européenne(d1)
        gamma = gamma_option_européenne(S, sigma, time, d1)
        theta = theta_call_option_européenne(S, sigma, time, K, risk_free_rate, d1, d2)
        rho = rho_call_option_européenne(time, K, risk_free_rate, d2)
        vega = vega_europe(S, time, d1) 
   
    elif callput == 3:
        Prix_Option = call_option_américaine(S, K, risk_free_rate, sigma, time)
        Text_Option = 'Prix option Call Américain: '
        delta = delta_call_option_européenne(d1)
        gamma = gamma_option_européenne(S, sigma, time, d1)
        theta = theta_call_option_européenne(S, sigma, time, K, risk_free_rate, d1, d2)
        rho = rho_call_option_européenne(time, K, risk_free_rate, d2)
        vega = vega_europe(S, time, d1) 
        
    elif callput == 2:
        Prix_Option = put_option_européenne(S, K, time, risk_free_rate, sigma)
        Text_Option = 'Prix option Put Européen: '
        delta = delta_put_option_européenne(d1)
        gamma = gamma_option_européenne(S, sigma, time, d1)
        theta = theta_put_option_européenne(S, sigma, time, K, risk_free_rate, d1, d2)
        rho = rho_put_option_européenne(time, K, risk_free_rate, d2)
        vega = vega_europe(S, time, d1)
        
    elif callput == 4:
        Prix_Option = put_option_américaine(S, K, risk_free_rate, sigma, time)
        Text_Option = 'Prix option Put Américain: '
        delta = delta_put_option_européenne(d1)
        gamma = gamma_option_européenne(S, sigma, time, d1)
        theta = theta_put_option_européenne(S, sigma, time, K, risk_free_rate, d1, d2)
        rho = rho_put_option_européenne(time, K, risk_free_rate, d2)
        vega = vega_europe(S, time, d1)
  
    # Ecriture des résultats dans la boîte de texte créee plus bas 
    T.delete(0.0, 'end') #delete permet d'effacer 
    
    # La fonction/méthode insert permet d'insérer des objets dans une liste
    T.insert(END, Text_Option) # affichage 
    T.insert(END, "%0.2f" % Prix_Option) # 0.2f permet de s'arréter à 4 chiffres apres la virgule 
    T.insert(END, "\n") # \n permet de faire des retours à la ligne 
    T.insert(END, "\nGreeks :")
    T.insert(END, "\ndelta: ")
    T.insert(END, "%0.2f" % delta)
    T.insert(END, "\ngamma: ")
    T.insert(END, "%0.2f" % gamma)
    T.insert(END, "\ntheta: ")
    T.insert(END, "%0.2f" % theta)
    T.insert(END, "\nrho: ")
    T.insert(END, "%0.2f" % rho)
    T.insert(END, "\nvega: ")
    T.insert(END, "%0.2f" % vega)   
    return

# Pricing des options
def call_option_européenne(S, K, time, risk_free_rate, sigma):
    call_price = S * norm.cdf(d1) - K * exp(-risk_free_rate*time)  * norm.cdf(d2)
    return call_price

def put_option_européenne(S, K, time, risk_free_rate, sigma):
    put_price = - S * norm.cdf(-d1) + K * exp(-risk_free_rate*time)  * norm.cdf(-d2)
    return put_price

def call_option_américaine(S, K, risk_free_rate, sigma, time): 
    Sp = float(S)
    Kt = float(K)
    v = float(sigma)
    T = float(time)
    r = float(risk_free_rate)
    N = 1000
    # Calcul des ratios de hausse et baisse, et création des listes contenant les stocks et srikes
    dt = T / N
    u = exp(v * sqrt(dt))
    d = 1.0 / u
    liste = list(range(N+1))
    liste2 = list(range(N+1))
    liste3 = list(range(N+1))
    liste2[0] = Sp * d**N
    # Boucles remplissant les listes avec les calcul des payoffs (liste), les stocks (liste2) et les strikes (liste3)
    for i in range(N+1):
        liste[i] = 0
        liste3[i] = Kt 
    for i in range(1, N, 1):
        liste2[i] =  u**2 * liste2[i-1]
    # Calcul du taux de actualisation et des probabilités de hausse et baisse
    a = exp(r * dt)
    pU = (a - d)/ (u - d)
    pD = 1.0 - pU
    # Remplissage de la liste avec les payoffs du call 
    for i in range(N):
        liste[i] = max(liste2[i]-liste3[i], 0.0)
    # Calcul du prix de l'option à l'instant T avec la technique de l'arbre binomiale (calcul inverse en fonction des payoffs)
    for i in range(N-1, -1, -1):
        for j in range(i):
            liste[j] = 1 / a * (pU * liste[j+1] + pD * liste[j])
            liste2[j] = d * liste2[j+1]
            liste[j] = max(liste[j], liste2[j]-liste3[j])
    return liste[0]

def put_option_américaine(S, K, risk_free_rate, sigma, time): 
    Sp = float(S)
    Kt = float(K)
    v = float(sigma)
    T = float(time)
    r = float(risk_free_rate)
    N = 2500
    
    dt = T / N
    u = exp(v * sqrt(dt))
    d = 1.0 / u
    liste = list(range(N+1))
    liste2 = list(range(N+1))
    liste3 = list(range(N+1))
    liste2[0] = Sp * d**N
 
    for i in range(N+1):
        liste[i] = 0
        liste3[i] = Kt 
    for i in range(1, N, 1):
        liste2[i] =  u**2 * liste2[i-1]

    a = exp(r * dt)
    pU = (a - d)/ (u - d)
    pD = 1.0 - pU

    for i in range(N):
        liste[i] = max(liste3[i]-liste2[i], 0.0)

    for i in range(N-1, -1, -1):
        for j in range(i):
            liste[j] = 1 / a * (pU * liste[j+1] + pD * liste[j])
            liste2[j] = d * liste2[j+1]
            liste[j] = max(liste[j], liste3[j]-liste2[j])
    return liste[0]

# Calcul des greques
def delta_call_option_européenne(d1):
    return norm.cdf(d1)

def delta_put_option_européenne(d1):
    return -(norm.cdf(-d1))
def gamma_option_européenne(S, sigma, time, d1):
    gamma = norm.pdf(d1) / (S * sigma * sqrt(time) )
    return gamma
def theta_call_option_européenne(S, sigma, time, K, risk_free_rate, d1, d2):
    theta = -(S * norm.pdf(d1) * sigma / (2 * sqrt(time))) - (risk_free_rate * K * exp(-risk_free_rate*time) * norm.cdf(d2))
    return theta
def theta_put_option_européenne(S, sigma, time, K, risk_free_rate, d1, d2):
    theta = -(S * norm.pdf(d1) * sigma / (2 * sqrt(time))) + (risk_free_rate * K * exp(-risk_free_rate*time) * norm.cdf(-d2))
    return theta
def rho_call_option_européenne(time, K, risk_free_rate, d2):
    rho = (time * K * exp(-risk_free_rate*time) * norm.cdf(d2))
    return rho

def rho_put_option_européenne(time, K, risk_free_rate, d2):
    rho = (-time * K * exp(-risk_free_rate*time) * norm.cdf(-d2))
    return rho
def vega_europe(S, time, d1):
    vega = (S * norm.pdf(d1) * sqrt(time))
    return vega

# Création d'un objet fenêtre ainsi que la définition de ses propriétés 
fenetre_BlackScholes_Binomial = Tk() # création de la fenêtre fenetre_BlackScholes_Binomial de la classe Tk()
# Définition des variables 
# StringVar() permet de créer une variable Tkinter
S = StringVar(); 
K = StringVar(); 
time = StringVar(); 
risk_free_rate = StringVar(); 
sigma = StringVar()
# Paramètres de la fenêtre
fenetre_BlackScholes_Binomial .title("Options Calculator") # définitiopn du titre donnée à la fenêtre 
fenetre_BlackScholes_Binomial .geometry("458x480+150+125") # définition de la dimension de la fenêtre 
lbl = Label(fenetre_BlackScholes_Binomial, text = "Choisir Option Call ou Put  Européenne/Américaines:",).pack(anchor=W)
# Définition des RadioBoutton qui permettra de choisir parmis un menu le type de pricing désiré
valeur = IntVar() # IntVar() permet de retourner un entier lorsqu'un boutton est choisi parmis 4 => ex: value = 1
Radiobutton(fenetre_BlackScholes_Binomial, text="Call Européen avec BlackScholes", padx = 40, variable=valeur, value=1).pack(anchor=W)
Radiobutton(fenetre_BlackScholes_Binomial, text="Put Européen avec BlackScholes", padx = 40, variable=valeur, value=2).pack(anchor=W)
Radiobutton(fenetre_BlackScholes_Binomial, text="Call Américain avec BinomialTree", padx = 40, variable=valeur, value=3).pack(anchor=W)
Radiobutton(fenetre_BlackScholes_Binomial, text="Put Américain avec BinomialTree", padx = 40, variable=valeur, value=4).pack(anchor=W)
# La méthode padx permet de laisser des espaces avant et après les bouttons 
# Pack(anchor=W) permet de placer 
# Dictionnaire avec les positions des labels 
Label_Position = { 'S' : [15, 130], 'K' : [15, 160], 'Maturity' :[15, 190], 'Risk' :[15, 220], 'Vol' :[15, 250]}
BtnPosX = 190
# Label est un objet graphique affichant du texte 

# Définition des entry boxes pour les paramètres des options
S_label = Label(fenetre_BlackScholes_Binomial, text = "S (prix sous-jacent): ")
S_label.place(x=Label_Position['S'][0], y=Label_Position['S'][1])
K_label = Label(fenetre_BlackScholes_Binomial, text = "K (K price ou prix exercé): ")
K_label.place(x=Label_Position['K'][0], y=Label_Position['K'][1])
Maturity_label = Label(fenetre_BlackScholes_Binomial, text = "T (Maturité) en années: ")
Maturity_label.place(x=Label_Position['Maturity'][0], y=Label_Position['Maturity'][1])
Risk_label = Label(fenetre_BlackScholes_Binomial, text = "r (Risk free) en décimales: ")
Risk_label.place(x=Label_Position['Risk'][0], y=Label_Position['Risk'][1])
Vol_Label = Label(fenetre_BlackScholes_Binomial, text = "V (Volatilité): ")
Vol_Label.place(x=Label_Position['Vol'][0], y=Label_Position['Vol'][1])
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
# Création des bouttons pour calculer les résultats (prix et lettres grecques) et quitter le programme 
bouton_calculer = Button(fenetre_BlackScholes_Binomial, text = "Cliquer pour donner les résultats : ",command = lecture_donnee)
bouton_calculer.place(x=5, y=300)
bouton_calculer.config(width=25, height=1)
# Création d'une fenêtre de texte qui affiche le prix de l'option 
T = Text(fenetre_BlackScholes_Binomial, height=9, width=32)
T.place(x=192, y=300)
# Lancer la fenêtre et la garder ouverte avec une boucle 
fenetre_BlackScholes_Binomial.mainloop()
