kill -9 $(lsof -t -i:7700)
source /home/security/dev/venvs/3.9/bin/activate
export FLASK_ENV=development
nohup flask run --port=7700 --host=0.0.0.0 >log 2>&1  &
