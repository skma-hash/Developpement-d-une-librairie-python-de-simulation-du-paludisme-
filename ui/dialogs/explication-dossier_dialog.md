# À Propos des Dialogs

## Définition

Les **dialogs** (fenêtres de dialogue) sont des **fenêtres secondaires** en Qt/PySide6 qui s'ouvrent temporairement par-dessus la fenêtre principale pour une tâche spécifique.

## Rôle des Dialogs dans votre projet

Le dossier `ui/dialogs/` contient des fenêtres secondaires pour :

### 1. **Configuration Avancée des Paramètres**

```
Fenêtre Principale (main_window.ui)
    ↓
[Bouton] "Advanced Parameters"
    ↓
Dialog: parameters_dialog.py (ou .ui)
├── Recovery Rate
├── Contact Rate
├── Incubation Period
└── [OK] [Cancel]
```

### 2. **Autres Usages Possibles**

- 📁 Charger/Sauvegarder des fichiers
- ⚙️ Configurer les solvers numérique
- 📊 Visualiser les résultats détaillés
- ✓ Confirmer des actions importantes

## Structure Actuelle

```
ui/
├── dialogs/
│   ├── __init__.py
│   └── parameters_dialog.py      ← Dialog pour paramètres avancés
├── main_window.py
└── main_window.ui
```

## Exemple d'Utilisation

### Dans `main.py`:

```python
from ui.dialogs.parameters_dialog import ParametersDialog

def open_advanced_parameters(self):
    """Ouvrir la fenêtre de paramètres avancés"""
    dialog = ParametersDialog(self)
    if dialog.exec() == QDialog.Accepted:
        # Récupérer les valeurs entrées
        recovery_rate = dialog.recovery_rate_spin.value()
        contact_rate = dialog.contact_rate_spin.value()
        print(f"Taux de récupération: {recovery_rate}")
```

## Types de Dialogs Courants

### 1. Dialog de Paramètres

```python
class ParametersDialog(QDialog):
    """Configuration des paramètres avancés"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Ajouter widgets de saisie
        # Ajouter boutons OK/Cancel
```

### 2. Dialog de Fichier

```python
# Intégré dans Qt
filepath = QFileDialog.getOpenFileName(self, "Ouvrir fichier")
filepath = QFileDialog.getSaveFileName(self, "Sauvegarder fichier")
```

### 3. Dialog de Message

```python
# Intégré dans Qt
QMessageBox.information(self, "Succès", "Simulation terminée!")
QMessageBox.warning(self, "Attention", "Vérifiez vos paramètres")
QMessageBox.critical(self, "Erreur", "Paramètres invalides")
```

## Avantages des Dialogs

✅ **Séparation des fonctionnalités**: Chaque dialog a sa responsabilité  
✅ **Réutilisabilité**: Dialogues utilisées dans plusieurs écrans  
✅ **Interface propre**: Pas de surcharge de la fenêtre principale  
✅ **Modularité**: Facile d'ajouter de nouveaux dialogs  
✅ **Expérience utilisateur**: Flux clair et intuitif

## Organiser vos Dialogs

```
ui/dialogs/
├── __init__.py
├── parameters_dialog.py         ← Paramètres avancés
├── parameters_dialog.ui         ← Design Qt Designer
├── results_dialog.py            ← Afficher résultats détaillés
├── settings_dialog.py           ← Préférences
└── about_dialog.py              ← À propos
```

## Connexion Dialog ↔ Main Window

```python
# main.py
def on_advanced_params_clicked(self):
    dialog = ParametersDialog(self)

    if dialog.exec() == QDialog.Accepted:
        # L'utilisateur a cliqué OK
        self.advanced_params = dialog.get_values()
        self.update_simulation()
    else:
        # L'utilisateur a cliqué Cancel
        pass
```

## Résumé

| Composant                      | Rôle                                       |
| ------------------------------ | ------------------------------------------ |
| `main_window.ui`               | Interface principale (large)               |
| `dialogs/parameters_dialog.ui` | Interface secondaire pour tâche spécifique |
| Fenêtre modale                 | Bloque l'interaction avec main_window      |
| `.exec()`                      | Attend la réponse de l'utilisateur         |

**En résumé**: Les dialogs sont des **fenêtres secondaires réutilisables** qui permettent une meilleure organisation et une interface plus propre! 🎯
