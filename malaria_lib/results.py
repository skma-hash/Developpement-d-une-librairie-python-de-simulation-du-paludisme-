import csv
import json
import simulation
# Recharger le module 'simulation' après modification du fichier source
import importlib
importlib.reload(simulation)


# Affectation du contenu du résultat de la fonction simulation.demo()
results = simulation.simulation_demo() 


# Ici c'est la fonction d'exportation des résultat sous divers formats 
def export_results_to_csv_json(results, csv_path='simulation_results.csv', json_path='simulation_results.json'):
    """Exporte les résultats de la simulation en JSON et CSV.

    - `results` : dictionnaire tel que retourné par `simulation_demo()`
    - `csv_path` : chemin du fichier CSV de sortie
    - `json_path` : chemin du fichier JSON de sortie
    """
    # Export JSON
    try:
        with open(json_path, 'w', encoding='utf-8') as fjson:
            json.dump(results, fjson, ensure_ascii=False, indent=2)
        print(f"✓ Résultats sauvegardés en JSON: {json_path}")
    except Exception as e:
        print(f"✗ Impossible d'écrire JSON: {e}")

    # Export CSV : on crée un tableau temps x variables
    keys_order = [
        't',
        'S11','V11','I11','S12','V12','I12','S13','V13','I13',
        'S_total','V_total','I_total','N_total','prevalence','couverture'
    ]
    available_keys = [k for k in keys_order if k in results]

    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as fcsv:
            writer = csv.writer(fcsv)
            writer.writerow(available_keys)

            n = len(results.get('t', []))
            for i in range(n):
                row = []
                for k in available_keys:
                    val = results[k][i] if isinstance(results[k], list) and i < len(results[k]) else results.get(k)
                    row.append(val)
                writer.writerow(row)

        print(f"✓ Résultats sauvegardés en CSV: {csv_path}")
    except Exception as e:
        print(f"✗ Impossible d'écrire CSV: {e}")

if __name__ == "__main__":
    if results is not None:
        csv_out = 'simulation_results.csv'
        json_out = 'simulation_results.json'
        export_results_to_csv_json(results, csv_path=csv_out, json_path=json_out)





# Ici c'est la fonction pour sauvegarder les résultats et les graphiques obtenus dans grace la fonction de simulation "simulation_demo()" (exemple) :

if results is not None:
    # CSV et JSON
    simulation.export_results_to_csv_json(results, csv_path='simulation_results.csv', json_path='simulation_results.json')
    # Graphiques : génère demo_sim.png et demo_sim.jpg dans le dossier courant
    simulation.export_plots(results, out_dir='.', prefix='demo_sim', formats=['png','jpg'])
else:
    print("Aucun résultat disponible pour l'export.")

