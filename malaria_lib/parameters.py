import csv
import os
from typing import Dict, Any, Union


def _to_number(s: str):
	"""Convertit une chaîne en int ou float si possible, sinon renvoie la chaîne d'origine."""
	if s is None:
		return None
	s = str(s).strip()
	if s == '':
		return None
	try:
		if '.' in s or 'e' in s.lower():
			return float(s)
		return int(s)
	except Exception:
		try:
			return float(s)
		except Exception:
			return s


def charger_parametres_csv(csv_path: str, as_instance: bool = True, validate: bool = True, raise_on_error: bool = True) -> Union[Dict[str, Any], object]:
	"""Charge des paramètres depuis un fichier CSV.

	Formats supportés :
	- fichier avec colonnes `name,value` (une ligne par paramètre)
	- fichier avec entêtes correspondant aux noms des paramètres et une seule ligne de valeurs
	- deux colonnes sans en-tête : première colonne = nom, seconde = valeur

	Si `as_instance=True`, la fonction importera `simulation.Parametres`, créera une instance
	et assignera les attributs trouvés. Sinon elle renverra un dictionnaire.

	Exemple d'utilisation :
	>>> params = load_parameters_from_csv('params.csv')
	>>> params_dict = load_parameters_from_csv('params.csv', as_instance=False)
	"""
	if not os.path.isfile(csv_path):
		raise FileNotFoundError(f"Fichier non trouvé: {csv_path}")

	with open(csv_path, newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		rows = list(reader)

	if not rows:
		raise ValueError('Fichier CSV vide')

	# Cas 1 : header contient 'name' et 'value' (ou 'param','val')
	header = [h.strip().lower() for h in rows[0]]
	params: Dict[str, Any] = {}

	if ('name' in header and 'value' in header) or ('param' in header and 'value' in header):
		# lire en tant que paires
		col_name = header.index('name') if 'name' in header else header.index('param')
		col_val = header.index('value')
		for r in rows[1:]:
			if len(r) <= max(col_name, col_val):
				continue
			name = r[col_name].strip()
			val = _to_number(r[col_val])
			if name:
				params[name] = val
	elif len(rows) >= 2 and all(c.strip() != '' for c in rows[0]):
		# Cas 2 : première ligne = entêtes, seconde ligne = valeurs
		keys = [k.strip() for k in rows[0]]
		vals = rows[1]
		for i, k in enumerate(keys):
			if i < len(vals):
				params[k] = _to_number(vals[i])
	else:
		# Cas 3 : deux colonnes sans header ou autres formats pairs
		for r in rows:
			if len(r) >= 2:
				name = r[0].strip()
				val = _to_number(r[1])
				if name:
					params[name] = val

	if as_instance:
		try:
			import simulation

			inst = simulation.Parametres()
			for k, v in params.items():
				# adapter quelques noms fréquents (facultatif)
				key = k.strip()
				if hasattr(inst, key):
					setattr(inst, key, v)
				else:
					# remplacer tirets ou espaces par underscore
					key2 = key.replace('-', '_').replace(' ', '_')
					if hasattr(inst, key2):
						setattr(inst, key2, v)
			# validation optionnelle
			if validate:
				errors = validate_params_dict({attr: getattr(inst, attr) for attr in vars(inst)}, raise_on_error=raise_on_error)
				if errors and not raise_on_error:
					print(" Erreurs de validation trouvées :")
					for e in errors:
						print(" - ", e)
			return inst
		except Exception as e:
			# si on ne peut pas créer l'instance, renvoyer le dict
			print(f" Impossible d'instancier simulation.Parametres: {e}. Retourne un dict.")
			return params

	return params


__all__ = ['charger_parametres_csv']


def validate_params_dict(params: Dict[str, Any], ranges: Dict[str, tuple] = None, raise_on_error: bool = True):
	"""Valide un dictionnaire de paramètres selon des plages fournies.

	- `params`: dict {name: value}
	- `ranges`: dict {name: (min, max)}; si None, on utilise des plages raisonnables par défaut
	- `raise_on_error`: si True, lève ValueError en cas d'erreur

	Retourne une liste d'erreurs (vide si OK)."""
	default_ranges = {
		'mu': (0.0, 1.0),
		'mu_v': (0.0, 1.0),
		'r': (0.0, 10.0),
		'd': (0.0, 1.0),
		'delta': (0.0, 1.0),
		'omega': (0.0, 1.0),
		'theta_1': (0.0, 1.0),
		'theta_2': (0.0, 1.0),
		'theta_3': (0.0, 1.0),
		'alpha_1': (0.0, 100.0),
		'alpha_2': (0.0, 100.0),
		'alpha_3': (0.0, 100.0),
		'beta': (0.0, 10.0),
		'c': (0.0, 1.0),
		'b_1': (0.0, 100.0),
		'b_2': (0.0, 100.0),
		'b_3': (0.0, 100.0),
	}
	if ranges is None:
		ranges = default_ranges

	errors = []
	for name, val in params.items():
		key = name.strip()
		if key in ranges:
			minv, maxv = ranges[key]
			try:
				if val is None:
					errors.append(f"Paramètre '{key}' est None")
					continue
				num = float(val)
			except Exception:
				errors.append(f"Paramètre '{key}' = {val!r} n'est pas numérique")
				continue
			if not (minv <= num <= maxv):
				errors.append(f"Paramètre '{key}' = {num} hors plage [{minv}, {maxv}]")

	if errors and raise_on_error:
		raise ValueError("Validation des paramètres échouée:\n" + "\n".join(errors))

	return errors
