import csv
import json
import simulation 

def exporter_resultats(resultats, nom_fichier, format="csv"):
    """
    Exporte les résultats dans un fichier CSV ou JSON.
    
    :param resultats: données à exporter (liste de dictionnaires ou objets simples)
    :param nom_fichier: nom du fichier de sortie (sans extension)
    :param format: 'csv' ou 'json'
    """
    if format.lower() == "csv":
        # Vérifier que resultats est une liste de dictionnaires
        if isinstance(resultats, list) and all(isinstance(r, dict) for r in resultats):
            with open(f"{nom_fichier}.csv", mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=resultats[0].keys())
                writer.writeheader()
                writer.writerows(resultats)
        else:
            raise ValueError("Pour CSV, les résultats doivent être une liste de dictionnaires.")

    elif format.lower() == "json":
        with open(f"{nom_fichier}.json", mode="w", encoding="utf-8") as f:
            json.dump(resultats, f, ensure_ascii=False, indent=4)

    else:
        raise ValueError("Format non supporté. Utilisez 'csv' ou 'json'.")


if __name__="__main__":
    exporter_resultats()

