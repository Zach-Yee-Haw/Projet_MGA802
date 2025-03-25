'''
Liste des matériaux disponible :    Class associée
    - Al 2024 T3                       Al_2024
    - Al 6061 T6                       Al_6061
    - Al 7075 T6                       Al_7075
    - Al (pure)                        Al
    - Cu (pure)                        Cu
    - Cu Cold Drawn (pure)             Cu_CD
    
Pour chacune de ces class, la fonction Info() donne toutes les informations 
concernant les propriétés physiques disponibles, leur valeur, leur unité
ainsi que la fonction associée
'''

class Al_2024:
    def __init__(self):
        pass
       
    def MasseVolumique(self):
        return 2780 # [kg/m^3]
    
    # Propriétés Mécaniques
    def ModuleYoung(self):
        return 73.1 # [GPa]

    def CoeffPoison(self):
        return 0.33
        
    def ModuleCisaillement(self):
        return 28 # [GPa]
    
    def LimiteCisaillement(self):
        return 283 # [MPa]

    def LimiteFatigue(self):
        return 138 # [MPa]

    def ResistanceTraction(self):
        return 483 # [MPa]

    def LimiteElastique(self):
        return 345 # [MPa]

    # Propriétés électriques
    def Resistivite(self):
        return 5.82*10**-8 # [Ohm.m]

    def Conductance(self):
        return 1/(5.82*10**-8) # [S/m]
    
    # Propriétés Thermiques
    def ThConductivite(self):
        return 121 # [W/m.K]
    
    def ChaleurSpe(self):
        return 875 # [J/kg/K]
    
    def Info(self):
        print('Propriétés Aluminium 2024-T3 :           unité    fonction')
        print('__________________________________________________________________________')
        print('Masse Volumique         ρ = 2780         kg/m^3   MasseVolumique()')
        print('Module de Young         E = 73.1         GPa      ModuleYoung()')
        print('Coefficient de Poison   ν = 0.33                  CoeffPoison()')
        print('Module de Cisaillement  G = 28           GPa      ModuleCisaillement()')
        print('Limite de Cisaillement    = 283          MPa      LimiteCisaillement()')
        print('Limite en Fatigue         = 138          MPa      LimiteFatigue()')
        print('Limite de Résistance  σ_u = 483          MPa      ResistanceTraction()')
        print('        en Traction')
        print('Limite Elastique      σ_Y = 345          MPa      LimiteElastique()')
        print('Résistivité électrique    = 5.82e-8      Ω.m      Resistivite()')
        print('Conductance électrique    = 17182130.58  S/m      Conductance()')
        print('Conductivité Thermique  λ = 121          W/m/K    ThConductivite()')
        print('Chaleur Spécifique      c = 875          J/kg/K   ChaleurSpe()')
#______________________________________________________________________________

class Al_6061:
    def __init__(self):
        pass
       
    def MasseVolumique(self):
        return 2700 # [kg/m^3]
    
    # Propriétés Mécaniques
    def ModuleYoung(self):
        return 68.9 # [GPa]

    def CoeffPoison(self):
        return 0.33
        
    def ModuleCisaillement(self):
        return 26 # [GPa]
    
    def LimiteCisaillement(self):
        return 207 # [MPa]

    def LimiteFatigue(self):
        return 96.5 # [MPa]

    def ResistanceTraction(self):
        return 310 # [MPa]

    def LimiteElastique(self):
        return 276 # [MPa]

    # Propriétés électriques
    def Resistivite(self):
        return 3.99*10**-8 # [Ohm.m]

    def Conductance(self):
        return 1/(3.99*10**-8) # [S/m]
    
    # Propriétés Thermiques
    def ThConductivite(self):
        return 167 # [W/m.K]
    
    def ChaleurSpe(self):
        return 896 # [J/kg/K]
    
    def Info(self):
        print('Propriétés Aluminium 6061-T6,6061-T651 : unité    fonction')
        print('__________________________________________________________________________')
        print('Masse Volumique         ρ = 2700         kg/m^3   MasseVolumique()')
        print('Module de Young         E = 68.9         GPa      ModuleYoung()')
        print('Coefficient de Poison   ν = 0.33                  CoeffPoison()')
        print('Module de Cisaillement  G = 26           GPa      ModuleCisaillement()')
        print('Limite de Cisaillement    = 207          MPa      LimiteCisaillement()')
        print('Limite en Fatigue         = 96.5         MPa      LimiteFatigue()')
        print('Limite de Résistance  σ_u = 310          MPa      ResistanceTraction()')
        print('        en Traction')
        print('Limite Elastique      σ_Y = 276          MPa      LimiteElastique()')
        print('Résistivité électrique    = 3.99e-8      Ω.m      Resistivite()')
        print('Conductance électrique    = 25062656.64  S/m      Conductance()')
        print('Conductivité Thermique  λ = 167          W/m/K    ThConductivite()')
        print('Chaleur Spécifique      c = 896          J/kg/K   ChaleurSpe()')
#______________________________________________________________________________

class Al_7075:
    def __init__(self):
        pass
       
    def MasseVolumique(self):
        return 2810 # [kg/m^3]
    
    # Propriétés Mécaniques
    def ModuleYoung(self):
        return 71.7 # [GPa]

    def CoeffPoison(self):
        return 0.33
        
    def ModuleCisaillement(self):
        return 26.9 # [GPa]
    
    def LimiteCisaillement(self):
        return 331 # [MPa]

    def LimiteFatigue(self):
        return 159 # [MPa]

    def ResistanceTraction(self):
        return 572 # [MPa]

    def LimiteElastique(self):
        return 503 # [MPa]

    # Propriétés électriques
    def Resistivite(self):
        return 5.15*10**-8 # [Ohm.m]

    def Conductance(self):
        return 1/(5.15*10**-8) # [S/m]
    
    # Propriétés Thermiques
    def ThConductivite(self):
        return 130 # [W/m.K]
    
    def ChaleurSpe(self):
        return 960 # [J/kg/K]
    
    def Info(self):
        print('Propriétés Aluminium 7075-T6;7075-T651 : unité    fonction')
        print('__________________________________________________________________________')
        print('Masse Volumique         ρ = 2810         kg/m^3   MasseVolumique()')
        print('Module de Young         E = 71.7         GPa      ModuleYoung()')
        print('Coefficient de Poison   ν = 0.33                  CoeffPoison()')
        print('Module de Cisaillement  G = 26.9         GPa      ModuleCisaillement()')
        print('Limite de Cisaillement    = 331          MPa      LimiteCisaillement()')
        print('Limite en Fatigue         = 159          MPa      LimiteFatigue()')
        print('Limite de Résistance  σ_u = 572          MPa      ResistanceTraction()')
        print('        en Traction')
        print('Limite Elastique      σ_Y = 503          MPa      LimiteElastique()')
        print('Résistivité électrique    = 5.15e-8      Ω.m      Resistivite()')
        print('Conductance électrique    = 19417475.73  S/m      Conductance()')
        print('Conductivité Thermique  λ = 130          W/m/K    ThConductivite()')
        print('Chaleur Spécifique      c = 960          J/kg/K   ChaleurSpe()')
#______________________________________________________________________________

class Al:
    def __init__(self):
        pass
       
    def MasseVolumique(self):
        return 2698.9 # [kg/m^3]
    
    # Propriétés Mécaniques
    def ModuleYoung(self):
        return 68 # [GPa]

    def CoeffPoison(self):
        return 0.36
        
    def ModuleCisaillement(self):
        return 25 # [GPa]
       
    # Propriétés électriques
    def Resistivite(self):
        return 2.7*10**-8 # [Ohm.m]

    def Conductance(self):
        return 1/(2.7*10**-8) # [S/m]
    
    # Propriétés Thermiques
    def ThConductivite(self):
        return 210 # [W/m.K]
    
    def ChaleurSpe(self):
        return 900 # [J/kg/K]
    
    def Info(self):
        print('Propriétés Aluminium (pure) :            unité    fonction')
        print('__________________________________________________________________________')
        print('Masse Volumique         ρ = 2698.9       kg/m^3   MasseVolumique()')
        print('Module de Young         E = 68           GPa      ModuleYoung()')
        print('Coefficient de Poison   ν = 0.36                  CoeffPoison()')
        print('Module de Cisaillement  G = 25           GPa      ModuleCisaillement()')
        print('Résistivité électrique    = 2.7e-8       Ω.m      Resistivite()')
        print('Conductance électrique    = 37037037.04  S/m      Conductance()')
        print('Conductivité Thermique  λ = 210          W/m/K    ThConductivite()')
        print('Chaleur Spécifique      c = 900          J/kg/K   ChaleurSpe()')
#______________________________________________________________________________

class Cu:
    def __init__(self):
        pass
       
    def MasseVolumique(self):
        return 8930 # [kg/m^3]
    
    # Propriétés Mécaniques
    def ModuleYoung(self):
        return 110 # [GPa]

    def CoeffPoison(self):
        return 0.343
        
    def ModuleCisaillement(self):
        return 46 # [GPa]
    
    def ResistanceTraction(self):
        return 210 # [MPa]

    def LimiteElastique(self):
        return 33.3 # [MPa]
 
    # Propriétés électriques
    def Resistivite(self):
        return 1.7*10**-8 # [Ohm.m]

    def Conductance(self):
        return 1/(1.7*10**-8) # [S/m]
    
    # Propriétés Thermiques
    def ThConductivite(self):
        return 385 # [W/m.K]
    
    def ChaleurSpe(self):
        return 385 # [J/kg/K]
    
    def Info(self):
        print('Propriétés Cuivre (pure) :               unité    fonction')
        print('__________________________________________________________________________')
        print('Masse Volumique         ρ = 8930         kg/m^3   MasseVolumique()')
        print('Module de Young         E = 110          GPa      ModuleYoung()')
        print('Coefficient de Poison   ν = 0.343                 CoeffPoison()')
        print('Module de Cisaillement  G = 46           GPa      ModuleCisaillement()')
        print('Limite de Résistance  σ_u = 210          MPa      ResistanceTraction()')
        print('        en Traction')
        print('Limite Elastique      σ_Y = 33.3         MPa      LimiteElastique()')
        print('Résistivité électrique    = 1.7e-8       Ω.m      Resistivite()')
        print('Conductance électrique    = 58823529.41  S/m      Conductance()')
        print('Conductivité Thermique  λ = 385          W/m/K    ThConductivite()')
        print('Chaleur Spécifique      c = 385          J/kg/K   ChaleurSpe()')
#______________________________________________________________________________

class Cu_CD:
    def __init__(self):
        pass
       
    def MasseVolumique(self):
        return 8930 # [kg/m^3]
    
    # Propriétés Mécaniques
    def ModuleYoung(self):
        return 110 # [GPa]

    def CoeffPoison(self):
        return 0.364
        
    def ModuleCisaillement(self):
        return 46 # [GPa]
    
    def ResistanceTraction(self):
        return 344 # [MPa]

    def LimiteElastique(self):
        return 333.4 # [MPa]
 
    # Propriétés électriques
    def Resistivite(self):
        return 1.7*10**-8 # [Ohm.m]

    def Conductance(self):
        return 1/(1.7*10**-8) # [S/m]
    
    # Propriétés Thermiques
    def ThConductivite(self):
        return 385 # [W/m.K]
    
    def ChaleurSpe(self):
        return 385 # [J/kg/K]
    
    def Info(self):
        print('Propriétés Cuivre Cold Drawn (pure) :    unité    fonction')
        print('__________________________________________________________________________')
        print('Masse Volumique         ρ = 8930         kg/m^3   MasseVolumique()')
        print('Module de Young         E = 110          GPa      ModuleYoung()')
        print('Coefficient de Poison   ν = 0.364                 CoeffPoison()')
        print('Module de Cisaillement  G = 46           GPa      ModuleCisaillement()')
        print('Limite de Résistance  σ_u = 344          MPa      ResistanceTraction()')
        print('        en Traction')
        print('Limite Elastique      σ_Y = 333.4        MPa      LimiteElastique()')
        print('Résistivité électrique    = 1.7e-8       Ω.m      Resistivite()')
        print('Conductance électrique    = 58823529.41  S/m      Conductance()')
        print('Conductivité Thermique  λ = 385          W/m/K    ThConductivite()')
        print('Chaleur Spécifique      c = 385          J/kg/K   ChaleurSpe()')
