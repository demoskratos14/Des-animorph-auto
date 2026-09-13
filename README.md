# Dés d'Aventure — application Android

Ce dépôt contient une appli Android complète qui embarque ton moteur de dés
(`dice_engine.py`), ton interface (`dice_web.py`) et ton image de fond
(`bg_animorph_data.py`) tels quels, grâce à **Chaquopy** (Python intégré
dans une appli Android).

## Ce que ça change par rapport à avant

Avant : il fallait lancer le script dans Pydroid 3, puis ouvrir manuellement
un navigateur sur `http://127.0.0.1:5001`.

Maintenant : un seul icône sur l'écran d'accueil. En le touchant,
l'application démarre elle-même le serveur en interne (invisible pour toi)
et affiche directement l'interface dans sa propre fenêtre. Aucun navigateur
externe ne s'ouvre — tout est géré par l'appli.

Concrètement :
- `MainActivity.kt` démarre Python au lancement, appelle
  `android_bridge.start_server()`, puis affiche une `WebView` (une fenêtre
  d'affichage web **intégrée à l'appli**, pas le navigateur du téléphone)
  pointée sur le serveur local.
- `android_bridge.py` (nouveau fichier) place la sauvegarde dans le
  stockage interne de l'appli (le seul endroit inscriptible sur Android) et
  démarre `dice_web.py` dans un thread.
- Ta sauvegarde `dice_state.json` fournie est copiée comme état de départ
  au tout premier lancement, pour ne pas repartir de zéro.
- Aucun fichier Python existant n'a été modifié dans sa logique : seule
  cette couche de démarrage a été ajoutée.
- L'icône fournie (`Icon.png`, deux dés) a été déclinée en toutes les
  résolutions nécessaires (`mipmap-mdpi` à `xxxhdpi`), y compris la version
  "icône adaptative" (Android 8+) qui sépare fond et premier plan pour
  s'adapter à la forme (rond, carré, arrondi...) de chaque téléphone. Le
  fond de l'icône reprend la couleur "papier" (`#FBF3E1`) de l'interface.

## Narration automatique (optionnelle)

Une carte "Narration automatique" est apparue sur la page principale. Elle
permet à l'appli d'écrire l'histoire toute seule à chaque lancer, sans
copier-coller manuel, en utilisant l'API gratuite de **Mistral AI**
(entreprise française) :

- Créer un compte gratuit sur [console.mistral.ai](https://console.mistral.ai/)
  (email + mot de passe, **sans carte bancaire**), puis générer une clé API.
- Coller cette clé dans la carte "Narration automatique" de l'appli.
- À partir de là, chaque lancer (et chaque utilisation de jauge
  totémique/allié) est automatiquement envoyé à l'IA, qui répond
  directement dans l'appli — l'histoire s'affiche au fil des lancers.

Détails techniques utiles à savoir :
- **Zéro dépendance ajoutée** : `mistral_client.py` (nouveau fichier)
  utilise uniquement `urllib` (bibliothèque standard Python), comme le
  reste du projet — aucun `pip install` supplémentaire n'était nécessaire
  côté Android, et le script reste utilisable tel quel dans Pydroid 3.
- La clé et toute la conversation avec l'IA sont sauvegardées comme le
  reste de la partie (`dice_state.json` en local sur l'appareil) — rien
  n'est envoyé ailleurs qu'à l'API Mistral officielle.
- Si l'appel à l'IA échoue (pas de réseau, clé invalide, quota du plan
  gratuit atteint...), le lancer de dés n'est **jamais perdu** : seul un
  petit message d'erreur s'affiche, et le bouton "copier le prompt
  complet" (mode manuel) reste disponible en secours.
- Un bouton "Réinitialiser la conversation IA" permet de repartir sur une
  conversation neuve avec le modèle sans toucher au reste de la partie
  (jauges, quêtes, historique des dés) — utile si la conversation devient
  très longue ou part dans une mauvaise direction. Seule une fenêtre
  récente de l'échange est de toute façon renvoyée au modèle à chaque
  appel (l'historique complet, lui, reste affiché et sauvegardé dans
  l'appli).
- Un bouton "Retirer la clé" repasse en mode manuel à tout moment.

## Nom de l'application et icône colorée

Cette version s'appelle **"Dés d'Aventure Auto"** (au lieu de "Dés
d'Aventure") et utilise un identifiant d'application différent
(`com.aventure.desdice.auto` au lieu de `com.aventure.desdice`). C'est ce
deuxième point qui compte vraiment pour Android : c'est lui qui décide si
une appli est "la même" (et donc mise à jour) ou une appli différente
(installée en plus). Avec un identifiant différent, tu peux donc garder
ton ancienne version installée et ajouter celle-ci à côté, sans que
l'une remplace l'autre.

L'icône a aussi été recolorée : les deux dés, qui étaient en noir uni,
sont maintenant dans un dégradé bleu → violet (les couleurs déjà
utilisées dans l'interface). La forme du dessin n'a pas changé, seule la
couleur — pratique aussi pour repérer cette version d'un coup d'œil sur
l'écran d'accueil, à côté de l'originale.

## Étape 1 — Créer le dépôt GitHub

1. Va sur [github.com/new](https://github.com/new) et crée un nouveau
   dépôt (public ou privé, peu importe), par exemple `des-aventure-app`.
   Ne coche aucune case (pas de README, pas de licence) : le dépôt doit
   être vide.
2. Sur ton ordinateur, dans le dossier de ce projet, exécute :

   ```bash
   git init
   git add .
   git commit -m "Première version de l'appli Android"
   git branch -M main
   git remote add origin https://github.com/<ton-compte>/des-aventure-app.git
   git push -u origin main
   ```

## Étape 2 — Laisser GitHub construire l'APK

Dès que le code est poussé sur la branche `main`, l'onglet **Actions** du
dépôt GitHub lance automatiquement le workflow `Build APK`
(`.github/workflows/build-apk.yml`). Il installe le SDK Android et Gradle,
compile le projet, puis met l'APK à disposition.

- Va dans l'onglet **Actions** du dépôt.
- Clique sur l'exécution la plus récente de "Build APK".
- En bas de la page, dans **Artifacts**, télécharge `des-aventure-apk`
  (un fichier `.zip` contenant `app-debug.apk`).

Si tu modifies le code plus tard et veux relancer un build sans nouveau
`push`, utilise le bouton **Run workflow** (déclenchement manuel) dans
l'onglet Actions.

## Étape 3 — Installer l'APK sur ton téléphone

1. Transfère `app-debug.apk` sur ton téléphone (câble, Drive, etc.).
2. Ouvre le fichier depuis le téléphone. Android demandera d'autoriser
   "l'installation d'applications inconnues" pour l'application utilisée
   pour ouvrir le fichier (ex. Fichiers, Chrome) — accepte pour cette
   installation.
3. Installe. Une icône "Dés d'Aventure" apparaît sur l'écran d'accueil.

## En cas d'échec du build sur GitHub

C'est un projet Android avec Python embarqué (Chaquopy) : la compilation
est plus lourde qu'une appli classique, et les versions des outils
(Chaquopy, Android Gradle Plugin, Gradle) évoluent avec le temps. Si le
workflow échoue :

1. Ouvre le détail de l'étape qui a échoué dans l'onglet Actions pour lire
   le message d'erreur exact.
2. Le plus souvent, c'est une histoire de versions à ajuster :
   - version de Chaquopy dans `build.gradle` (racine) et `app/build.gradle`
   - version d'Android Gradle Plugin dans `build.gradle` (racine)
   - version de Gradle dans le workflow (`gradle-version`)
   - la page officielle [chaquo.com/chaquopy/doc/current/versions.html](https://chaquo.com/chaquopy/doc/current/versions.html)
     donne les combinaisons compatibles.
3. Tu peux aussi coller le message d'erreur ici dans la conversation, je
   pourrai ajuster les fichiers en conséquence.

## Structure du projet

```
des-aventure-app/
├── .github/workflows/build-apk.yml   # construit l'APK automatiquement
├── build.gradle                      # plugins Android/Kotlin/Chaquopy
├── settings.gradle
├── gradle.properties
├── gradle/wrapper/gradle-wrapper.properties
└── app/
    ├── build.gradle                  # config Android + dépendance "flask" via pip
    ├── proguard-rules.pro
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/aventure/desdice/MainActivity.kt
        ├── res/                      # nom de l'appli, layout, icônes (mipmap-*)
        └── python/
            ├── dice_engine.py        # ton moteur, inchangé (+ narration auto)
            ├── dice_web.py           # ton interface Flask, inchangée (+ narration auto)
            ├── mistral_client.py     # nouveau : client API Mistral (stdlib pure)
            ├── bg_animorph_data.py   # ton image de fond, inchangée
            ├── android_bridge.py     # nouveau : démarre le serveur en interne
            └── dice_state_seed.json  # ta sauvegarde de départ (copiée au 1er lancement)
```

## Ouvrir le projet dans Android Studio (optionnel)

Si tu veux modifier le projet toi-même avant de le repousser sur GitHub :
ouvre le dossier avec Android Studio (menu *Open*). Au premier lancement,
Android Studio proposera de régénérer le fichier `gradle-wrapper.jar`
manquant (nécessaire seulement en local, pas pour le build GitHub) —
accepte, ou lance `gradle wrapper --gradle-version 8.7` une fois si tu as
Gradle installé sur ta machine.
