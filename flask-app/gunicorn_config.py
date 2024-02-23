# to run -> gunicorn -c gunicorn_config.py main:app

bind = '0.0.0.0:8000'  # Replace with the desired bind address and port
workers = 4  # Adjust the number of workers as needed
daemon = True # to run the program in background
