export FLASK_ENV=development
source /home/security/dev/venvs/3.9/bin/activate
kill -9 $(lsof -t -i:7701)
flask run --port=7701 --host=0.0.0.0
