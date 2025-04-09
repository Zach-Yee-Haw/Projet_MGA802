import matplotlib.pyplot as plt
import matplotlib
import streamlit as st

matplotlib.use('Qt5Agg')
import numpy as np
import plotly as ply
import plotly.express as px
import plotly.graph_objects as go

def Resistance(L,S,res):
    '''
    Permet de calculer la résistance électrique d'un câble dont on connait les
    dimensions et le matériau qui le compose
    
    Attributs :
        - L (float)     Longueur du câble                               [m]
        - S (float)     Surface de la section du câble                  [m²]
        - res (float)   Résistivité électrique du matériau du câble     [Ohm.m]
    
    Sortie :
        - R (float)     Résistance électrique du câble                  [Ohm]
    '''
    R = res*L/S
    return R
#______________________________________________________________________________
    
def Volume(L,S):
    '''
    Permet de calculer le volume du câble dont on connait les dimensions
    
    Attributs :
        - L (float)     Longueur du câble               [m]
        - S (float)     Surface de la section du câble  [m²]
    
    Sortie :
        - Vol (float)   Volume du câble                 [m^3]
    '''
    Vol = L*S
    return Vol
#______________________________________________________________________________   
    
def Masse(Vol,rho):
    '''
    Permet de calculer la masse du câble dont on connait les caractéristiques
    
    Attributs :
        - Vol (float)   Volume du câble                 [m^3]
        - rho (float)   Masse volumique du matériau     [kg/m^3]
        
    Sortie :
        - m (float)     Masse du câble                  [kg]
    '''
    m = Vol*rho
    return m
#______________________________________________________________________________

def Mat2Liste(cable,m):
    '''
    Permet de discrétiser un câble rectiligne défini par une matrice contenant 
    les points au extrémité du câble. 
    
    Cette fonction est la réciproque de Liste2Mat()
    
    Attributs :
        - cable (array) (2,3)   Coordonnées des extrémités de câble     [m]
        - m (int)               Nombre de points de discrétisation      []
    
    Sorties : 
        - x (array) (m,)        Liste des abscisses des points du câble [m]
        - y (array) (m,)        Liste des ordonnées des points du câble [m]
        - z (array) (m,)        Liste des côtes des points du câble     [m]
    '''
    x = np.linspace(cable[0][0],cable[1][0],m)
    y = np.linspace(cable[0][1],cable[1][1],m)
    z = np.linspace(cable[0][2],cable[1][2],m)
    return x,y,z
 
#______________________________________________________________________________
  
def Liste2Mat(x,y,z):
    '''
    Permet de transformer un câble rectiligne défini par des listes de coordonnées
    en une matrice qui contient les coordonnées des extrémités du câble
    
    Cette fonction est la réciproque de Mat2Liste()
    
    Attributs :
        - x (array) (m,)        Liste des abscisses des points du câble [m]
        - y (array) (m,)        Liste des ordonnées des points du câble [m]
        - z (array) (m,)        Liste des côtes des points du câble     [m]
        
    Sortie :
        - cable (array) (2,3)   Coordonnées des extrémités du câble     [m]
    '''
    cable = np.array([[x[0],y[0],z[0]],[x[-1],y[-1],z[-1]]])
    return cable
#______________________________________________________________________________

def Graph(x, y, z, titre=None, F_i=None, B_i=None, colonne = None):
    '''
    Permet de tracer dans un repère 3D un câble défini par des listes de coordonnées
    en afficant les vecteurs du champ magnétique (B) et de la force EM (F_EM)
    
    Attributs :
        - x (array) (m,)        Liste des abscisses des points du câble [m]
        - y (array) (m,)        Liste des ordonnées des points du câble [m]
        - z (array) (m,)        Liste des côtes des points du câble     [m]
        - titre (str)           Titre du graphique
        - F_i (list) (m,3)      Liste des F_EM pour chaque point        [N]
        - B_i (list) (m,3)      Liste des B pour chaque point           [T]
        
    Sortie : 
        - Graph du câble dans le repère du satellite avec les vecteurs de B et F_EM
    '''
    x = np.array(x)
    y = np.array(y) 
    z = np.array(z)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    # Compute axis limits
    x_range = np.max(x) - np.min(x)
    y_range = np.max(y) - np.min(y)
    z_range = np.max(z) - np.min(z)
    max_range = max(x_range, y_range, z_range)

    # Set equal aspect ratio
    ax.set_xlim(np.min(x), np.min(x) + max_range)
    ax.set_ylim(np.min(y), np.min(y) + max_range)
    ax.set_zlim(np.min(z), np.min(z) + max_range)
    #ax.set_box_aspect([x_range, y_range, z_range])  # Preserve aspect ratio
    
    ax.plot(x, y, z, label='Câble', linewidth = 2)
    ax.scatter(0, 0, 0, color='red',label='Satellite' ,s=100)
    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Z [m]')
    
    if titre == None :
        ax.set_title('Câble Paramétré en 3D')
    else :
        ax.set_title(titre)
    
    B_i = np.array(B_i) if B_i is not None else None
    F_i = np.array(F_i) if F_i is not None else None
    multiplier = 1e4 # can be changed to better visualize F_EM_i
    
    # Plot vectors
    if F_i is not None and F_i.any():
        ax.quiver(x, y, z, F_i[:, 0], F_i[:, 1], F_i[:, 2], 
                  length=multiplier, normalize=False, color='red', 
                  label=r'$\vec{F}_{EM}$ [N]')
    
    if B_i is not None and B_i.any():
        ax.quiver(x, y, z, B_i[:, 0], B_i[:, 1], B_i[:, 2], 
                  length=100.0, normalize=True, color='green', 
                  label=r'$\vec{B}$ [T]')    
    plt.legend()

    plyfig = go.Figure(data=go.Scatter3d(
        x=x, y=y, z=z,
        marker = dict(size = 1,
                      color = "cyan"),
        line = dict(color = "cyan",
                    width = 2),
        name = "Câble"))
    plyfig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        marker = dict(size = 4,
                      color = "red"),
        name = "Satellite"))


    if colonne == None:

        st.plotly_chart(plyfig)
    else:
        with colonne:
            st.plotly_chart(plyfig)