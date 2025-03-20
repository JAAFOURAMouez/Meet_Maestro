#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions pour la gestion des réunions Google Meet
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException

from config.constants import (
    NAME_INPUT_SELECTOR, 
    JOIN_BUTTON_XPATH, 
    WAITING_ROOM_XPATH,
    QUIT_BUTTON_SELECTOR,
    INITIAL_WAIT,
    NAME_ENTRY_WAIT,
    HOST_ACCEPTANCE_WAIT
)

# Récupération du logger
logger = logging.getLogger("MeetMaestro")

def join_meeting(driver, meet_url):
    """Rejoint une réunion Google Meet"""
    try:
        logger.info(f"Accès à l'URL: {meet_url}")
        driver.get(meet_url)
        
        # Ajouter un délai initial pour permettre le chargement complet de la page
        time.sleep(INITIAL_WAIT)
        
        # Saisie du nom
        logger.info("Attente du champ de saisie du nom...")
        nom = driver.find_element(By.XPATH, NAME_INPUT_SELECTOR)
        nom.clear()
        nom.send_keys('Meet Maestro Bot')
        logger.info("Nom 'Meet Maestro Bot' saisi avec succès")
        
        # Attendre un peu après avoir entré le nom
        time.sleep(NAME_ENTRY_WAIT)
        
        try:
            # Rechercher le bouton Rejoindre
            join_button = driver.find_element(By.XPATH, JOIN_BUTTON_XPATH)
            join_button.click()
            logger.info("Bouton Rejoindre cliqué avec succès")
        except NoSuchElementException:
            logger.error("Impossible de cliquer sur le bouton Rejoindre")
            raise Exception("Bouton 'Rejoindre' introuvable")
        
        time.sleep(20)

        # Attendre que l'hôte accepte ou vérifier si déjà dans la réunion
        try:
            logger.info("Attente de l'acceptation par l'hôte...")
            WebDriverWait(driver, HOST_ACCEPTANCE_WAIT).until_not(
                EC.presence_of_element_located((By.XPATH, WAITING_ROOM_XPATH))
            )
            logger.info("Hôte accepté, réunion lancée.")
            return True
        except TimeoutException:
            logger.error("Délai d'attente dépassé pour l'acceptation par l'hôte")
            driver.save_screenshot('timeout_join.png')
            return False

    except Exception as e:
        logger.error(f"Échec de la connexion : {e}")
        driver.save_screenshot('error_join.png')
        return False

def quit_meeting(driver):
    """Quitte proprement la réunion Google Meet"""
    try:
        logger.info("Tentative de quitter la réunion...")
        quit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, QUIT_BUTTON_SELECTOR)))
        quit_button.click()
        logger.info("Réunion quittée avec succès.")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la tentative de quitter la réunion : {e}")
        return False

def check_meeting_active(driver):
    """Vérifie si la réunion est toujours active"""
    try:
        # Rechercher le bouton quitter
        try:
            driver.find_element(By.CSS_SELECTOR, QUIT_BUTTON_SELECTOR)
            return True
        except (NoSuchElementException, WebDriverException):
            logger.info(f"bouton quitter introuvable")
            return False
    except Exception as e:
        logger.error(f"Erreur lors de la vérification de l'état de la réunion: {e}")
        # Par sécurité, on suppose que la réunion est toujours active
        return True
    
