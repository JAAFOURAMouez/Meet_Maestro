#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions utilitaires pour le navigateur Chrome
"""

from selenium.webdriver.chrome.options import Options

def get_chrome_options():
    """Configure les options Chrome pour Meet"""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Options supplémentaires pour améliorer la stabilité
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Options pour contourner les détections d'automatisation
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-browser-side-navigation")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Autoriser les permissions audio/vidéo automatiquement
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1,
        "profile.default_content_setting_values.popups": 2
    })
    
    return options