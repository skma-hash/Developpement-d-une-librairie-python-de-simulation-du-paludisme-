#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Démonstration simple du modèle de paludisme
Version simplifiée pour test rapide
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Paramètres du modèle
class Parametres:
    def __init__(self):
        # Paramètres démographiques
        self.mu = 0.00004    # Mortalité humaine
        self.mu_v = 0.1      # Mortalité moustiques
        self.r = 0.1         # Naissance moustiques
        self.d = 0.005       # Mortalité paludisme
        
        # Paramètres épidémiologiques
        self.delta = 0.05    # Guérison
        self.omega = 0.002   # Perte immunité
        
        # Vaccination
        self.theta_1 = 0.01  # Matin
        self.theta_2 = 0.005 # Soirée
        self.theta_3 = 0.001 # Nuit
        
        # Transitions
        self.alpha_1 = 3.0
        self.alpha_2 = 3.0
        self.alpha_3 = 3.0
        
        # Transmission
        self.beta = 0.5
        self.c = 0.3
        self.b_1 = 0.5
        self.b_2 = 1.0
        self.b_3 = 2.0

# Système d'équations simplifié (seulement Groupe 1)
def systeme_equations(t, y, params):
    """Système simplifié avec 9 équations (Groupe 1 seulement)"""
    
    # Variables: S11, V11, I11, S12, V12, I12, S13, V13, I13
    S11, V11, I11, S12, V12, I12, S13, V13, I13 = y
    
    # Population vectorielle fixe pour simplifier
    Nv = 50000
    Iv = 5000  # 10% infectés
    
    # Forces d'infection
    lambda1 = params.beta * params.b_1 * params.c * Iv / Nv
    lambda2 = params.beta * params.b_2 * params.c * Iv / Nv
    lambda3 = params.beta * params.b_3 * params.c * Iv / Nv
    
    # Équations différentielles
    dS11_dt = (10 + params.alpha_3 * S13 + params.omega * V11 + params.delta * I11) - \
              (params.mu * S11 + params.alpha_1 * S11 + lambda1 * S11)
    
    dV11_dt = (params.theta_1 * S11 + params.alpha_3 * V13 + 5) - \
              (params.mu * V11 + params.omega * V11 + params.alpha_1 * V11)
    
    dI11_dt = (lambda1 * S11 + params.alpha_3 * I13 + 1) - \
              ((params.d + params.mu) * I11 + params.delta * I11 + params.alpha_1 * I11)
    
    dS12_dt = (10 + params.alpha_1 * S11 + params.omega * V12 + params.delta * I12) - \
              (params.mu * S12 + params.alpha_2 * S12 + lambda2 * S12)
    
    dV12_dt = (params.theta_2 * S12 + params.alpha_1 * V11 + 5) - \
              (params.mu * V12 + params.omega * V12 + params.alpha_2 * V12)
    
    dI12_dt = (lambda2 * S12 + params.alpha_1 * I11 + 1) - \
              ((params.d + params.mu) * I12 + params.delta * I12 + params.alpha_2 * I12)
    
    dS13_dt = (10 + params.alpha_2 * S12 + params.omega * V13 + params.delta * I13) - \
              (params.mu * S13 + params.alpha_3 * S13 + lambda3 * S13)
    
    dV13_dt = (params.theta_3 * S13 + params.alpha_2 * V12 + 5) - \
              (params.mu * V13 + params.omega * V13 + params.alpha_3 * V13)
    
    dI13_dt = (lambda3 * S13 + params.alpha_2 * I12 + 1) - \
              ((params.d + params.mu) * I13 + params.delta * I13 + params.alpha_3 * I13)
    
    return [dS11_dt, dV11_dt, dI11_dt, dS12_dt, dV12_dt, dI12_dt, 
            dS13_dt, dV13_dt, dI13_dt]

def simulation_demo():
    """Exécute une simulation de démonstration"""
    print("=== DÉMONSTRATION MODÈLE PALUDISME ===")
    
    # Paramètres
    params = Parametres()
    
    # Conditions initiales (Groupe 1 seulement)
    y0 = [
        3000, 500, 100,  # Phase 1: S11, V11, I11
        3000, 500, 100,  # Phase 2: S12, V12, I12
        3000, 500, 100   # Phase 3: S13, V13, I13
    ]
    
    # Temps de simulation
    t_span = (0, 100)  # 100 jours
    t_eval = np.linspace(0, 100, 200)
    
    print("Démarrage de la simulation...")
    
    # Résolution
    try:
        sol = solve_ivp(
            fun=lambda t, y: systeme_equations(t, y, params),
            t_span=t_span,
            y0=y0,
            t_eval=t_eval,
            method='RK45',
            rtol=1e-6
        )
        
        if sol.success:
            print("✓ Simulation réussie!")
            
            # Extraction des résultats
            t = sol.t
            S11, V11, I11, S12, V12, I12, S13, V13, I13 = sol.y
            
            # Calculs dérivés
            S_total = S11 + S12 + S13
            V_total = V11 + V12 + V13
            I_total = I11 + I12 + I13
            N_total = S_total + V_total + I_total
            
            prevalence = I_total / N_total
            couverture = V_total / N_total
            
            # Affichage des résultats finaux
            print(f"\nRésultats finaux (jour {t[-1]:.0f}):")
            print(f"Population totale: {N_total[-1]:.0f}")
            print(f"Susceptibles: {S_total[-1]:.0f} ({S_total[-1]/N_total[-1]*100:.1f}%)")
            print(f"Vaccinés: {V_total[-1]:.0f} ({couverture[-1]*100:.1f}%)")
            print(f"Infectés: {I_total[-1]:.0f} ({prevalence[-1]*100:.1f}%)")
            
            # Graphiques
            plt.figure(figsize=(12, 8))
            
            # Graphique 1: Évolution des compartiments
            plt.subplot(2, 2, 1)
            plt.plot(t, S_total, 'g-', label='Susceptibles', linewidth=2)
            plt.plot(t, V_total, 'b-', label='Vaccinés', linewidth=2)
            plt.plot(t, I_total, 'r-', label='Infectés', linewidth=2)
            plt.xlabel('Temps (jours)')
            plt.ylabel('Population')
            plt.title('Évolution des compartiments')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Graphique 2: Prévalence et couverture
            plt.subplot(2, 2, 2)
            plt.plot(t, prevalence * 100, 'r-', label='Prévalence (%)', linewidth=2)
            plt.plot(t, couverture * 100, 'b-', label='Couverture vaccinale (%)', linewidth=2)
            plt.xlabel('Temps (jours)')
            plt.ylabel('Pourcentage')
            plt.title('Indicateurs épidémiologiques')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Graphique 3: Infectés par phase
            plt.subplot(2, 2, 3)
            plt.plot(t, I11, 'g-', label='Matin (I₁₁)', linewidth=2)
            plt.plot(t, I12, 'orange', label='Soirée (I₁₂)', linewidth=2)
            plt.plot(t, I13, 'r-', label='Nuit (I₁₃)', linewidth=2)
            plt.xlabel('Temps (jours)')
            plt.ylabel('Infectés')
            plt.title('Infectés par phase temporelle')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Graphique 4: Population totale
            plt.subplot(2, 2, 4)
            plt.plot(t, N_total, 'k-', label='Population totale', linewidth=2)
            plt.xlabel('Temps (jours)')
            plt.ylabel('Population')
            plt.title('Évolution de la population totale')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('demo_simulation.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print(f"\n✓ Graphiques sauvegardés dans 'demo_simulation.png'")
            
            return sol
            
        else:
            print(f"✗ Échec de la simulation: {sol.message}")
            return None
            
    except Exception as e:
        print(f"✗ Erreur lors de la simulation: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    simulation_demo()