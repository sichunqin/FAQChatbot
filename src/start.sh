kill -9 $(lsof -t -i:7700)
export FLASK_ENV=development
nohup flask run --port=7700 --host=0.0.0.0 >log 2>&1  &
