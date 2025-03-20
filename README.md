# Meet Maestro

## Bot d'infiltration pour Google Meet

Meet Maestro est un bot qui peut rejoindre automatiquement une réunion Google Meet, jouer un fichier audio directement via le microphone dans la réunion, puis quitter automatiquement à la fin de l'audio.

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
- PyAudio pour la redirection audio (voir Installation)

## Installation

1. Cloner ce dépôt
2. Créer les dossiers nécessaires :
   ```
   mkdir -p config utils
   touch config/__init__.py utils/__init__.py
   ```
3. Installer les dépendances principales : 
   ```
   pip install selenium playsound webdriver-manager
   ```
4. Installer PyAudio pour la redirection audio :
   - **Windows** : `pip install pyaudio wave numpy`
   - **macOS** : `brew install portaudio` puis `pip install pyaudio wave numpy`
   - **Linux** : `sudo apt-get install python3-pyaudio` puis `pip install wave numpy`

## Fonctionnement Audio

Le programme redirige automatiquement l'audio du fichier directement vers le microphone :

1. Il détecte le microphone par défaut de votre système
2. Il crée un flux audio qui redirige le son du fichier vers ce microphone
3. Google Meet capte ce son comme s'il venait naturellement du microphone

## Fonctionnalités

- **Raccrocher interrompt l'audio** : Si vous quittez la réunion, l'audio s'arrête immédiatement
- **Ctrl+C interrompt l'audio** : Vous pouvez arrêter le programme à tout moment
- **Détection intelligente** : Le bot détecte automatiquement si vous avez quitté la réunion
- **Multiple formats audio** : Compatibilité avec les fichiers WAV et autres formats supportés

## Utilisation

### Utilisation simple

```bash
python maestro.py
```

Le bot va automatiquement :
1. Lancer Chrome
2. Rejoindre la réunion Google Meet spécifiée
3. Activer le microphone si nécessaire
4. Lire le fichier audio directement sur le microphone
5. Quitter la réunion une fois l'audio terminé

### Avec des arguments

Vous pouvez spécifier l'URL de la réunion et le fichier audio via des arguments :

```bash
python maestro.py --meet_url="https://meet.google.com/abc-defg-hij" --audio_file="presentation.wav"
```

Options disponibles :
- `--meet_url` : URL de la réunion Google Meet à rejoindre
- `--audio_file` : Chemin vers le fichier audio à jouer

### Aide

Pour voir toutes les options disponibles :

```bash
python maestro.py --help
```

## Messages "underrun occurred"

Les messages ALSA "underrun occurred" sont normaux sous Linux et n'indiquent pas un problème majeur. Ils signifient simplement que le tampon audio s'est vidé temporairement, ce qui est courant lors de la redirection audio.

## Résolution des problèmes

Si vous rencontrez des problèmes avec l'audio:

1. Vérifiez que le microphone est activé dans Google Meet
2. Vérifiez que Chrome a la permission d'accéder au microphone
3. Consultez le fichier de log "meet_maestro.log" pour plus de détails
4. Si l'installation de PyAudio échoue :
   - Windows: Essayez `pip install pipwin` puis `pipwin install pyaudio`
   - macOS: Assurez-vous que portaudio est installé avec brew
   - Linux: Utilisez `sudo apt-get install python3-pyaudio`

## Notes importantes

- Les sélecteurs XPath ont été configurés spécifiquement pour l'interface actuelle de Google Meet et ne doivent pas être modifiés.
- Aucune configuration manuelle de périphériques audio virtuels n'est nécessaire, tout se fait automatiquement.