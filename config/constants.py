#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Constantes et configurations pour Meet Maestro
"""

# Sélecteurs - Ne pas modifier car ils fonctionnent bien
QUIT_BUTTON_SELECTOR = 'button[aria-label*="Quitter l\'appel"], button[aria-label*="Leave call"]'
NAME_INPUT_SELECTOR = '/html/body/div[1]/c-wiz/div/div/div[38]/div[4]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[1]/div[3]/div[1]/span[2]/input'
WAITING_TEXT_XPATH = '//span[contains(text(), "En attente")]'
JOIN_BUTTON_XPATH = '//*[@id="yDmH0d"]/c-wiz/div/div/div[38]/div[4]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div/button/span[6]'
WAITING_ROOM_XPATH = '/html/body/div[1]/c-wiz/div/div/div[38]/div[4]/div/div[2]/div[4]/div/div/div[2]/div[3]'

# Valeurs par défaut
DEFAULT_AUDIO_FILE = "test.wav"
DEFAULT_MEET_URL = "https://meet.google.com/qwn-jzgr-ztx"

# Paramètres de délais (en secondes)
INITIAL_WAIT = 2
NAME_ENTRY_WAIT = 1
HOST_ACCEPTANCE_WAIT = 60
INTERFACE_LOAD_WAIT = 5
AUDIO_START_WAIT = 2
INACTIVE_CHECK_THRESHOLD = 3
POLL_INTERVAL = 1