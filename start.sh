if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/marsel7official/SAFARI-PREMIUMbot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /SAFARI-PREMIUMbot
fi
cd /SAFARI-PREMIUMbot
pip3 install -U -r requirements.txt
echo "Starting SAFARI-PREMIUMbot...."
python3 bot.py
