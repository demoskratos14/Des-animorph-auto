# -*- coding: utf-8 -*-
"""
Pont entre l'application Android (Kotlin) et le serveur Flask existant.

Ce module est appele une seule fois au demarrage de l'appli (depuis
MainActivity.kt). Il :
  1. Place le repertoire de travail sur le stockage interne de l'appli
     (os.environ["HOME"], fourni automatiquement par Chaquopy), qui est
     le seul endroit inscriptible sur Android.
  2. Copie la sauvegarde initiale (dice_state.json fournie au depart)
     UNIQUEMENT si aucune sauvegarde n'existe encore, pour ne pas ecraser
     une aventure deja en cours.
  3. Importe dice_web (qui cree l'objet Flask "app") et le lance dans un
     thread en arriere-plan, sur 127.0.0.1:5001.

Le WebView de MainActivity charge ensuite directement cette adresse : tout
se passe a l'interieur de l'application, sans jamais ouvrir de navigateur
externe.
"""

import os
import shutil
import threading
from os.path import dirname, join, exists

_started = False
_lock = threading.Lock()


def start_server():
    global _started
    with _lock:
        if _started:
            return "already_running"
        _started = True

        home = os.environ["HOME"]
        os.chdir(home)

        save_path = join(home, "dice_state.json")
        if not exists(save_path):
            seed_path = join(dirname(__file__), "dice_state_seed.json")
            if exists(seed_path):
                shutil.copyfile(seed_path, save_path)

        import dice_web  # cree/charge la session au moment de l'import

        def _run():
            dice_web.app.run(
                host="127.0.0.1",
                port=5001,
                debug=False,
                use_reloader=False,
                threaded=True,
            )

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        return "started"
