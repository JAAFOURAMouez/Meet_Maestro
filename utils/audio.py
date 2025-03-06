#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions pour la gestion audio du bot Meet Maestro
"""

import logging
import threading
from config.constants import DEFAULT_AUDIO_FILE

# Variable globale pour suivre l'état de l'audio et le fichier audio
audio_finished = threading.Event()
audio_file = DEFAULT_AUDIO_FILE

# Récupération du logger
logger = logging.getLogger("MeetMaestro")

def set_audio_file(file_path):
    """Définit le fichier audio à utiliser"""
    global audio_file
    audio_file = file_path

def get_audio_file():
    """Retourne le fichier audio en cours d'utilisation"""
    global audio_file
    return audio_file

def play_audio():
    """Joue le fichier audio et signale quand il est terminé"""
    try:
        from playsound import playsound
        logger.info(f"Début de la lecture audio: {audio_file}")
        playsound(audio_file)
        logger.info("Lecture audio terminée.")
    except ImportError:
        logger.error("Module playsound non disponible. Installation requise: pip install playsound")
    except Exception as e:
        logger.error(f"Erreur lors de la lecture audio : {e}")
    finally:
        # Indiquer que l'audio est terminé
        audio_finished.set()