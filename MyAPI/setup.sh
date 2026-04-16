---

### 2. Le Script d'Installation  `setup.sh`

```bash
#!binbash

echo Début de l'installation de l'environnement API Agentic...

# 1. VérificationInstallation de Docker
if ! [ -x $(command -v docker) ]; then
  echo Installation de Docker...
  if [[ $OSTYPE == darwin ]]; then
    echo Merci d'installer Docker Desktop via  httpswww.docker.comproductsdocker-desktop
  else
    curl -fsSL httpsget.docker.com -o get-docker.sh
    sudo sh get-docker.sh
  fi
else
  echo Docker est déjà installé.
fi

# 2. Installation de decK (CLI Kong)
echo Installation de decK...
if [[ $OSTYPE == darwin ]]; then
  brew install kongtapdeck
else
  curl -sL httpsgithub.comkongdeckreleasesdownloadv1.39.1deck_1.39.1_linux_amd64.tar.gz  tar xz
  sudo mv deck usrlocalbin
fi

# 3. Installation de Node.js et Prism (pour le Mocking)
echo Installation de Prism via NPM...
if ! [ -x $(command -v npm) ]; then
    echo Node.js non trouvé. Installation en cours...
    # Installation rapide via nvm ou gestionnaire de paquets
    curl -fsSL httpsdeb.nodesource.comsetup_lts.x  sudo -E bash -
    sudo apt-get install -y nodejs
fi
sudo npm install -g @stoplightprism-cli

# 4. Installation des dépendances Python pour les Agents
echo Configuration de l'environnement Python...
python3 -m venv venv
source venvbinactivate
pip install chromadb openai langchain flask

echo Installation terminée avec succès.
echo Pour démarrer le projet  docker-compose up -d