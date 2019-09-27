Initialisation de Heroku 
------------------------

Exporter la liste des paquetages requis :
pip freeze > requirements.txt

Supprimer les entrées suivantes :
mkl-fft
mkl-random
mkl-service

heroku login
heroku git:remote -a rc-tagging
git add .
git commit -m "Message"
git push heroku master

Initialisation de GitHub
------------------------

git init
git remote add github https://github.com/RegisC/taggingserver.git
git push github master


Pour afficher les messages émis sur le serveur
----------------------------------------------

heroku logs -t


Adresse du serveur web
----------------------

https://rc-tagging.herokuapp.com/predict


Exécution locale
----------------

conda activate 

RunFlask.bat
ou
ipython AutomaticTagging.py
ou 
waitress-serve --port=5000  app:instance


