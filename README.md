# Meet Maestro

## Bot d'infiltration pour Google Meet

Meet Maestro est un bot qui peut rejoindre automatiquement une réunion Google Meet, jouer un fichier audio dans la réunion, puis quitter automatiquement à la fin de l'audio.

## Structure du projet

```
meet-maestro/
├── maestro.py              # Script principal
├── config/
│   ├── __init__.py
│   └── constants.py        # Constantes et configurations
├── utils/
│   ├── __init__.py
│   ├── audio.py            # Fonctions pour la gestion audio
│   ├── browser.py          # Configuration du navigateur
│   └── meeting.py          # Fonctions de gestion des réunions
├── requirements.txt        # Dépendances du projet
└── README.md               # Documentation
```

## Prérequis

- Python 3.6+
- Google Chrome
- Un fichier audio (par défaut "test.wav" dans le dossier racine)

## Installation

1. Cloner ce dépôt
2. Créer les dossiers nécessaires :
   ```
   mkdir -p config utils
   touch config/__init__.py utils/__init__.py
   ```
3. Installer les dépendances : 
   ```
   pip install -r requirements.txt
   ```

## Utilisation

### Utilisation simple

```
python maestro.py
```

Le bot va automatiquement :
1. Lancer Chrome
2. Rejoindre la réunion Google Meet spécifiée
3. Lire le fichier audio
4. Quitter la réunion une fois l'audio terminé

### Avec des arguments

Vous pouvez spécifier l'URL de la réunion et le fichier audio via des arguments :

```
python maestro.py --meet_url="https://meet.google.com/abc-defg-hij" --audio_file="presentation.wav"
```

Options disponibles :
- `--meet_url` : URL de la réunion Google Meet à rejoindre
- `--audio_file` : Chemin vers le fichier audio à jouer

### Aide

Pour voir toutes les options disponibles :

```
python maestro.py --help
```

## Fonctionnalités

- Rejoint automatiquement une réunion Google Meet
- Joue un fichier audio pendant la réunion
- Détecte la fin de l'audio et quitte automatiquement
- Détecte si l'utilisateur quitte manuellement la réunion
- Journalise toutes les actions pour faciliter le débogage

## Notes importantes

- Les sélecteurs XPath ont été configurés spécifiquement pour l'interface actuelle de Google Meet et ne doivent pas être modifiés.
- Si vous rencontrez des problèmes, consultez le fichier de log "meet_maestro.log" pour plus de détails.