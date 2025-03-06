#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Meet Maestro - Bot d'infiltration Google Meet
Script principal pour contrôler le bot
"""

import sys
import os
import time
import logging
import threading
import argparse
from selenium import webdriver

# Import des modules internes
from config.constants import DEFAULT_AUDIO_FILE, DEFAULT_MEET_URL
from utils.browser import get_chrome_options
from utils.audio import play_audio, audio_finished, set_audio_file
from utils.meeting import join_meeting, quit_meeting, check_meeting_active

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("meet_maestro.log")
    ]
)
logger = logging.getLogger("MeetMaestro")

def parse_arguments():
    """Parse les arguments de ligne de commande"""
    parser = argparse.ArgumentParser(description="Meet Maestro - Bot pour Google Meet")
    
    parser.add_argument("--meet_url", 
                        help="URL de la réunion Google Meet",
                        default=DEFAULT_MEET_URL)
    
    parser.add_argument("--audio_file", 
                        help="Chemin vers le fichier audio à jouer",
                        default=DEFAULT_AUDIO_FILE)
    
    return parser.parse_args()

def main():
    """Fonction principale du Meet Maestro Bot"""
    # Récupérer les arguments de ligne de commande
    args = parse_arguments()
    
    # Définir les paramètres à partir des arguments
    meet_url = args.meet_url
    audio_file = args.audio_file
    
    # Mettre à jour le fichier audio dans le module audio
    set_audio_file(audio_file)
    
    # Vérifier l'existence du fichier audio
    if not os.path.exists(audio_file):
        logger.error(f"Fichier audio {audio_file} introuvable.")
        print(f"ERREUR: Fichier audio {audio_file} introuvable.")
        sys.exit(1)
    
    logger.info(f"Utilisation de l'URL: {meet_url}")
    logger.info(f"Utilisation du fichier audio: {audio_file}")
    
    # Initialiser le navigateur
    logger.info("Initialisation du navigateur Chrome...")
    driver = None
    
    try:
        try:
            driver = webdriver.Chrome(options=get_chrome_options())
            logger.info("Chrome initialisé sans Service")
        except Exception as e3:
            logger.error(f"Toutes les méthodes d'initialisation ont échoué: {e3}")
            raise Exception("Impossible d'initialiser Chrome après plusieurs tentatives")
        
        # Vérifier si le driver a été correctement initialisé
        if driver is None:
            raise Exception("Driver non initialisé")     
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du navigateur : {e}")
        print("ERREUR: Impossible de démarrer le navigateur Chrome.")
        sys.exit(1)
    
    try:
        # Tenter de rejoindre la réunion
        if not join_meeting(driver, meet_url):
            print("ERREUR: Impossible de rejoindre la réunion.")
            sys.exit(1)
        
        # Attendre que l'interface de la réunion soit complètement chargée
        logger.info("Attente de chargement complet de l'interface Meet...")
        time.sleep(5)
                
        # Lancer l'audio dans un thread séparé
        logger.info("Démarrage du thread audio...")
        audio_thread = threading.Thread(target=play_audio)
        audio_thread.daemon = True  # Le thread s'arrêtera si le programme principal s'arrête
        audio_thread.start()
        
        # Attendre que l'audio démarre
        time.sleep(2)
        
        # Vérifier immédiatement si la réunion est active
        if not check_meeting_active(driver):
            logger.warning("La réunion semble inactive juste après la connexion - vérification...")
            # Réessayer après un court délai
            time.sleep(3)
            if not check_meeting_active(driver):
                logger.error("Réunion inactive après double vérification. Capture d'écran prise.")
                driver.save_screenshot('meeting_inactive.png')
            else:
                logger.info("Réunion active après double vérification.")
        
        # Boucle principale: surveiller l'état de la réunion et de l'audio
        logger.info("Surveillance de la réunion...")
        check_count = 0
        consecutive_inactive = 0
        
        while True:
            # Incrémenter le compteur
            check_count += 1
            
            # Vérifier si l'utilisateur a quitté manuellement (avec plus de tolérance)
            if not check_meeting_active(driver):
                consecutive_inactive += 1
                logger.warning(f"Réunion potentiellement inactive ({consecutive_inactive}/3)")
                
                # Ne considérer la réunion comme inactive qu'après 3 vérifications consécutives
                if consecutive_inactive >= 3:
                    logger.info("L'utilisateur a quitté la réunion (3 vérifications consécutives)")
                    print("Réunion terminée par l'utilisateur.")
                    break
            else:
                # Réinitialiser le compteur si la réunion est active
                consecutive_inactive = 0
            
            # Log périodique pour confirmer que la surveillance est active
            if check_count % 10 == 0:
                logger.info(f"Surveillance en cours... ({check_count} vérifications)")
            
            # Vérifier si l'audio est terminé
            if audio_finished.is_set():
                logger.info("Audio terminé, quitter la réunion...")
                quit_meeting(driver)
                break
            
            # Pause pour éviter une utilisation CPU excessive
            time.sleep(1)
        
        # Attendre un instant pour voir le message de fin de réunion
        time.sleep(2)
    
    except KeyboardInterrupt:
        logger.info("Programme interrompu par l'utilisateur.")
        print("\nProgramme interrompu par l'utilisateur.")
    except Exception as e:
        logger.error(f"Erreur principale : {e}")
        print(f"ERREUR: {e}")
    finally:
        # S'assurer que le navigateur se ferme correctement
        logger.info("Fermeture du navigateur...")
        driver.quit()
        print("Programme terminé.")

if __name__ == "__main__":
    main()