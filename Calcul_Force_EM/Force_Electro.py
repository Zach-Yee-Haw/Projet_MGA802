import numpy as np
import Calcul_Force_EM.Satellite as Satellite
import Calcul_Force_EM.ChampMagnetique as cm

'''
Ce code contient des fonctions qui permettent de calculer la force électrodynamique
générée par un câble conducteur baigné dans un champ magnétique.

La fonction ForceELectro() permet de calculer cette force sur un segment rectiligne

La fonction Discret() permet de calculer cette force sur un segment que l'on va discrétiser
pour plus de précision. Cette fonction utilise les données du module ppigrf et
réalise donc les calculs avec le champ magnétique terrestre

La fonction Parametre() fonctionne sur le même principe que la fonction Discret()
mais cette fois-ci pour des courbes quelconques
'''

#______________________________________________________________________________

def ForceElectro(B, cable, I, V, R):
    '''
    Permet de calculer la force de Lorentz générée par un câble conducteur, 
    de résistance électrique R, parcouru par un courant I, baigné dans un 
    champ magnétique B et se déplaçant à la vitesse V.
    
    - Le câble considéré doit être rectiligne
    
    Attributs :
        - B (array) (3,)        Champ magnétique                        [T]
        - cable (array) (2,3)   Coordonnées des extrémités de câble     [m]
        - I (float or None)     Intensité du courant                    [A]
        - V (float)             Vitesse de déplacement du câble         [m/s]
        - R (float)             Résistance électrique du câble          [Ohm]

    Sortie :
        - F_mag                 Force de Lorentz résultante            [N]
    '''
    V = np.array([V,0,0])
        
    # Calcul du vecteur longueur du câble, orienté positivement en direction du satellite
    L = -np.array([cable[1][0]-cable[0][0], cable[1][1]-cable[0][1], cable[1][2]-cable[0][2]])
    l = np.linalg.norm(L) # Norme du vecteur longueur du câble = Longueur du câble

    # Cas du courant induit
    if I == None : 
        E = np.cross(V,B)        # Calcul du champ électrique induit
        U = np.dot(E,L)          # Calcul de la tension générée dans le câble
        U = np.squeeze(U)
        I = (U/R)*L/l            # Calcul du vecteur courant induit
        F_mag = l*np.cross(I,B)  # Calcul de la force électrodynamique
            
    # Cas du courant imposé
    else:
        In = I*L/l               # Calcul du vecteur courant
        F_mag = l*np.cross(In,B) # Calcul de la force électrodynamique

    return F_mag

#______________________________________________________________________________

def Discret(r, theta, phi, date, INC, TA, cable, m, I, V, R):
    '''
    Permet de calculer la force de Lorentz générée par un câble conducteur, 
    de résistance électrique R, parcouru par un courant I, baigné dans un 
    champ magnétique et se déplaçant à la vitesse V.
    
    - Le champ magnétique considéré ici est celui de la Terre
    
    - Le câble considéré doit être rectiligne et il sera discrétisé en m segments.
      Il doit être exprimé dans le repère du satellite
    
    - Le satellite, de coordonnées sphériques (r,θ,φ), ainsi que son anomalie vraie
      et l'inclinaison de son orbite doivent être exprimées dans le repère 
      terrestre ECEF
    
    Attributs :
        - r (float)             Coordonnée selon r du satellite         [km]
        - theta (float)         Coordonnée selon θ du satellite         [deg]
        - phi (float)           Coordonnée selon φ du satellite         [deg]
        - date (datetime)       Date de calcul 
        - INC (float)           Inclinaison de l'orbite du satellite    [deg]
        - TA (float)            Anomalie vraie du satellite             [deg]
        - cable (array) (2,3)   Coordonnées des extrémités de câble     [m]
        - m (int)               Nombre de points de discrétisation      []
        - I (float or None)     Intensité du courant                    [A]
        - V (float)             Vitesse de déplacement du câble         [m/s]
        - R (float)             Résistance électrique du câble          [Ohm]

    Sortie :
        - F_mag                 Force de Lorentz résultante            [N]
    '''
    # Pas de discrétisation selon x, y et z, dans le repère du satellite
    px = (cable[1][0] - cable[0][0])/m
    py = (cable[1][1] - cable[0][1])/m
    pz = (cable[1][2] - cable[0][2])/m
        
    Li = [] # Liste des points de discrétisation
    Bi = [] # Liste des champs magnétique aux différents points de discrétisation
    V = np.array([V,0,0]) # Vecteur vitesse
    F_mag = 0 # Force Electrodynamique      
    Sat = np.array([[r], [theta], [phi]]) # Vecteur position du satellite dans ECEF
        
    for i in range(m):
        Li.append([cable[0][0] + i*px , cable[0][1] + i*py , cable[0][2] + i*pz])
        P = Satellite.Sat2Earth(Li[i][0], Li[i][1], Li[i][2], INC, TA, Sat)
        B0 = cm.ChampMagnetique(P[0], P[1], P[2], date)
        B0 = Satellite.Earth2Sat_cm(B0[0], B0[1], B0[2], INC, TA)
        Bi.append(B0)
        
    Li.append(cable[1])
        
    L = -np.array([Li[1][0]-Li[0][0], Li[1][1]-Li[0][1], Li[1][2]-Li[0][2]])
    l = np.linalg.norm(L)

    # Cas du courant induit
    if I == None :
        U = 0  # Tension dans le câble
        '''
        Cette première boucle a pour but de calculer toutes les tensions induites sur les
        segments de discrétisation, dans le but d'en déduire le courant induit qui parcourt 
        tout le câble
        '''
        for i in range(m):
            E = np.cross(V,Bi[i]) # Calcul du champ électrique induit
            U2 = np.dot(E,L)      # Calcul de la tension induite dans le segment i
            U2 = np.squeeze(U2)
            U = U + U2
            
        I2 = (U/R)   # Calcul du courant induit dans le câble
        In = I2* L/l # Calcul du vecteur courant sur les segments
        'Calcul de la somme des force Electrodynamique sur chaque segments'
        for i in range(m):     
            F_mag = F_mag + l*np.cross(In,Bi[i])
        
    # Cas du courant imposé
    else :
        In = I*L/l # Calcul du vecteur courant sur les segments
        for i in range(m):
            F_mag = F_mag + l*np.cross(In,Bi[i])
        
    return F_mag

#______________________________________________________________________________


def Parametre(r, theta, phi, date, INC, TA, X_cable, Y_cable, Z_cable, I, V, R):
    '''
    Permet de calculer la force de Lorentz générée par un câble conducteur, 
    de résistance électrique R, parcouru par un courant I, baigné dans un 
    champ magnétique et se déplaçant à la vitesse V.
    
    - Le champ magnétique considéré ici est celui de la Terre
    
    - Le câble est ici défini par les trois liste X_cable, Y_cable et Z_cable,
      qui contiennent les coordonnées des points qui définissent le câble,
      exprimées dans le repère du satellite
    
    - Le calcul se fait ici de façon discrète entre chaque point du câble
    
    - Le satellite, de coordonnées sphériques (r,θ,φ), ainsi que son anomalie vraie
      et l'inclinaison de son orbite doivent être exprimées dans le repère 
      terrestre ECEF
    
    Attributs :
        - r (float)             Coordonnée selon r du satellite         [km]
        - theta (float)         Coordonnée selon θ du satellite         [deg]
        - phi (float)           Coordonnée selon φ du satellite         [deg]           
        - date (datetime)       Date de calcul 
        - INC (float)           Inclinaison de l'orbite du satellite    [deg]
        - TA (float)            Anomalie vraie du satellite             [deg]
        - X_cable (array) (h,1) Liste des abscisses des points du câble  [m]
        - Y_cable (array) (h,1) Liste des ordonnées des points du câble [m]
        - Z_cable (array) (h,1) Liste des côtes des points du câble     [m]
                    h étant la longueur de ces listes
        - I (float or None)     Intensité du courant                    [A]
        - V (float)             Vitesse de déplacement du câble         [m/s]
        - R (float)             Résistance électrique du câble          [Ohm]

    Sortie :
        - F_mag                 Force de Lorentz résultante            [N]
    '''
    n = len(X_cable) # Nombre de points de discrétisation
    Cable = []       # Liste des coordonnées des différents points de discrétisation 
    Bi = [] # Liste du champ magnétique aux différents points
    V = np.array([V,0,0]) # Vecteur vitesse
    F_mag = 0 # Force Electrodynamique 
    Sat = np.array([[r], [theta], [phi]]) # Vecteur position du satellite dans ECEF
        
    for i in range(n):
        Cable.append(np.array([X_cable[i], Y_cable[i], Z_cable[i]]))
        P = Satellite.Sat2Earth(Cable[i][0], Cable[i][1], Cable[i][2], INC, TA, Sat)
        B0 = cm.ChampMagnetique(P[0], P[1], P[2], date)
        B0 = Satellite.Earth2Sat_cm(B0[0], B0[1], B0[2], INC, TA)
        Bi.append(B0)
        
    L = [] # Liste des vecteurs longueurs du câble sur les segments de discrétisation, orientés positivement en direction du satellite
    l = [] # Liste des normes des segments de discrétisations
    F_mag_i_vect = np.zeros(3) # Liste des forces EM (x,y,z) pour chaque segment de discrétisation
    
    # Cas du courant induit
    if I == None :
        U = 0  # Tension dans le câble
        '''
        Cette première boucle a pour but de calculer toutes les tensions induites sur les
        segments de discrétisation, dans le but d'en déduire le courant induit qui parcourt 
        tout le câble
        '''
        for i in range(n-1):
            L.append(-np.array([Cable[i+1][0]-Cable[i][0], Cable[i+1][1]-Cable[i][1], Cable[i+1][2]-Cable[i][2]]))
            l.append(np.linalg.norm(L[i]))
        
            E = np.cross(V,Bi[i]) # Calcul du champ électrique induit
            U2 = np.dot(E,L[i])   # Calcul de la tension induite dans le segment i
            U2 = np.squeeze(U2)
            U = U + U2
            
        I2 = (U/R) # Calcul du courant induit dans le câble
            
        'Calcul de la somme des force Electrodynamique sur chaque segments'
        for i in range(n-1):   
            In = I2* L[i]/l[i] # Calcul du vecteur courant sur le segment i
            F_mag_i = l[i]*np.cross(In,Bi[i])
            F_mag_i_vect = np.vstack((F_mag_i_vect, F_mag_i))
            F_mag = F_mag + F_mag_i
           
    # Cas du courant imposé        
    else :
        for i in range(n-1):
            L.append(-np.array([Cable[i+1][0]-Cable[i][0], Cable[i+1][1]-Cable[i][1], Cable[i+1][2]-Cable[i][2]]))
            l.append(np.linalg.norm(L[i]))

            In = I*L[i]/l[i] # Calcul du vecteur courant sur le segment i
            F_mag_i = l[i]*np.cross(In,Bi[i])
            F_mag_i_vect = np.vstack((F_mag_i_vect, F_mag_i))
            F_mag = F_mag + F_mag_i
            
    return F_mag, Bi, F_mag_i_vect
