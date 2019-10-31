#!/bin/bash

echo "  ____  __ __  ______   ___   _____ ____  _       ___  ____  ______ ";
echo " /    ||  |  ||      | /   \ / ___/|    \| |     /   \|    ||      |";
echo "|  o  ||  |  ||      ||     (   \_ |  o  ) |    |     ||  | |      |";
echo "|     ||  |  ||_|  |_||  O  |\__  ||   _/| |___ |  O  ||  | |_|  |_|";
echo "|  _  ||  :  |  |  |  |     |/  \ ||  |  |     ||     ||  |   |  |  ";
echo "|  |  ||     |  |  |  |     |\    ||  |  |     ||     ||  |   |  |  ";
echo "|__|__| \__,_|  |__|   \___/  \___||__|  |_____| \___/|____|  |__|  ";
echo "                                                                    ";

function installDebian () {
    sudo apt-get update;
    sudo apt-get -y install git python2.7 python-pip postgresql apache2;
    pip2 install requests psutil;
    installMSF;
}

function installFedora () {
    sudo yum -y install git python-pip;
    pip2 install requests psutil;
    installMSF;
}

function installOSX () {
  xcode-select --install;
  /usr/bin/ruby -e "$(curl -fsSkL raw.github.com/mxcl/homebrew/go)";
  echo PATH=/usr/local/bin:/usr/local/sbin:$PATH >> ~/.bash_profile;
  source ~/.bash_profile;
  brew tap homebrew/versions;
  brew install nmap;
  brew install homebrew/versions/ruby21;
  gem install bundler;
  brew install postgresql --without-ossp-uuid;
  initdb /usr/local/var/postgres;
  mkdir -p ~/Library/LaunchAgents;
  cp /usr/local/Cellar/postgresql/9.4.4/homebrew.mxcl.postgresql.plist ~/Library/LaunchAgents/;
  launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist;
  createuser msf -P -h localhost;
  createdb -O msf msf -h localhost;
  installOsxMSF;
}

function installOsxMSF () {
  mkdir /usr/local/share;
  cd /usr/local/share/;
  git clone https://github.com/rapid7/metasploit-framework.git;
  cd metasploit-framework;
  for MSF in $(ls msf*); do ln -s /usr/local/share/metasploit-framework/$MSF /usr/local/bin/$MSF;done;
  sudo chmod go+w /etc/profile;
  sudo echo export MSF_DATABASE_CONFIG=/usr/local/share/metasploit-framework/config/database.yml >> /etc/profile;
  bundle install;
  echo "[!!] A DEFAULT CONFIG OF THE FILE 'database.yml' WILL BE USED";
  rm /usr/local/share/metasploit-framework/config/database.yml;
  cat > /usr/local/share/metasploit-framework/config/database.yml << '_EOF'
production:
  adapter: postgresql
  database: msf
  username: msf
  password:
  host: 127.0.0.1
  port: 5432
  pool: 75
  timeout: 5
_EOF
  source /etc/profile;
  source ~/.bash_profile;
}

function installMSF () {
    if [[ ! "$(which msfconsole)" = */* ]]; then
        curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && \
            chmod 755 msfinstall && \
            ./msfinstall;
        rm msfinstall;
    fi
}

function install () {
    case "$(uname -a)" in
        *Debian*|*Ubuntu*)
            installDebian;
            ;;
        *Fedora*)
            installFedora;
            ;;
        *Darwin*)
            installOSX;
            ;;
        *)
            echo "Unable to detect an operating system that is compatible with AutoSploit...";
            ;;
    esac
    echo "";
    echo "Installation Complete";
}

install;
