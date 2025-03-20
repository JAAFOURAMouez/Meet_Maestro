#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions pour la gestion audio du bot Meet Maestro
Utilisation de PyAudio pour rediriger l'audio directement vers le micro
"""

import logging
import threading
import os
import time
from config.constants import DEFAULT_AUDIO_FILE

# Variable globale pour suivre l'état de l'audio et le fichier audio
audio_finished = threading.Event()
audio_file = DEFAULT_AUDIO_FILE

# Ajout d'un event pour interrompre l'audio quand l'utilisateur raccroche
stop_audio = threading.Event()

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

def interrupt_audio():
    """Interrompt la lecture audio en cours"""
    global stop_audio
    logger.info("Interruption de la lecture audio demandée")
    stop_audio.set()

def reset_audio_state():
    """Réinitialise l'état de l'audio pour une nouvelle utilisation"""
    global audio_finished, stop_audio
    audio_finished.clear()
    stop_audio.clear()

def play_audio():
    """
    Joue le fichier audio directement vers le microphone.
    Utilise PyAudio pour lire le fichier et l'envoyer vers l'entrée du micro.
    """
    global stop_audio
    stop_audio.clear()  # S'assurer que l'état est réinitialisé
    
    try:
        import pyaudio
        import wave
        import numpy as np
        
        logger.info(f"Lecture de l'audio {audio_file} directement vers le microphone...")
        
        # Ouvrir le fichier audio
        wf = wave.open(audio_file, 'rb')
        
        # Initialiser PyAudio
        p = pyaudio.PyAudio()
        
        # Afficher les informations sur les périphériques disponibles
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        
        # Trouver le périphérique d'entrée (microphone)
        input_device_index = None
        for i in range(numdevices):
            device_info = p.get_device_info_by_index(i)
            if device_info.get('maxInputChannels') > 0:
                logger.info(f"Périphérique d'entrée trouvé: {device_info.get('name')} (index: {i})")
                if "default" in device_info.get('name').lower() or i == p.get_default_input_device_info().get('index'):
                    input_device_index = i
                    logger.info(f"Sélection du périphérique d'entrée par défaut: {device_info.get('name')}")
                    break
        
        if input_device_index is None:
            # Si aucun périphérique par défaut n'est trouvé, prendre le premier périphérique d'entrée
            for i in range(numdevices):
                device_info = p.get_device_info_by_index(i)
                if device_info.get('maxInputChannels') > 0:
                    input_device_index = i
                    logger.info(f"Sélection du premier périphérique d'entrée disponible: {device_info.get('name')}")
                    break
        
        if input_device_index is None:
            logger.error("Aucun périphérique d'entrée trouvé. Impossible de rediriger l'audio.")
            raise Exception("Aucun périphérique d'entrée trouvé")
            
        # Créer un stream pour lire le fichier audio
        sample_format = p.get_format_from_width(wf.getsampwidth())
        channels = wf.getnchannels()
        rate = wf.getframerate()
        
        # Stream de sortie (pour les haut-parleurs si nécessaire)
        output_stream = p.open(format=sample_format,
                               channels=channels,
                               rate=rate,
                               output=True)
        
        # Stream d'entrée (pour le microphone)
        input_stream = p.open(format=sample_format,
                              channels=channels,
                              rate=rate,
                              input=False,
                              output=True,
                              output_device_index=input_device_index)
        
        logger.info(f"Configuration des streams audio - Taux: {rate}Hz, Canaux: {channels}")
        
        # Lire et envoyer les données
        chunk_size = 1024
        data = wf.readframes(chunk_size)
        
        while len(data) > 0 and not stop_audio.is_set():
            # Vérifier si l'audio doit être interrompu
            if stop_audio.is_set():
                logger.info("Interruption de la lecture audio détectée")
                break
            
            # Envoyer les données aux deux streams
            output_stream.write(data)  # Pour les haut-parleurs
            input_stream.write(data)   # Pour le microphone
            data = wf.readframes(chunk_size)
        
        # Attendre que toutes les données soient jouées
        if not stop_audio.is_set():
            time.sleep(0.5)
        
        # Fermer les streams
        output_stream.stop_stream()
        output_stream.close()
        input_stream.stop_stream()
        input_stream.close()
        
        # Fermer PyAudio
        p.terminate()
        
        # Fermer le fichier wave
        wf.close()
        
        if stop_audio.is_set():
            logger.info("Lecture audio interrompue.")
        else:
            logger.info("Lecture audio terminée avec succès.")
        
    except ImportError:
        logger.error("Module PyAudio non disponible. Installation requise: pip install pyaudio wave numpy")
        
        # Fallback sur playsound si PyAudio n'est pas disponible
        try:
            from playsound import playsound
            logger.info(f"Fallback: Lecture audio via playsound: {audio_file}")
            playsound(audio_file)
            logger.info("Lecture audio terminée (playsound).")
        except Exception as e:
            logger.error(f"Erreur lors de la lecture avec playsound: {e}")
            
    except Exception as e:
        logger.error(f"Erreur lors de la lecture audio : {e}")
        
    finally:
        # Indiquer que l'audio est terminé
        audio_finished.set()