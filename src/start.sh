export FLASK_ENV=development
nohup flask run --port=7700 --host=0.0.0.0 >log 2>&1  &
