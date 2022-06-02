name = "serialnumberupload"
workers = 4
bind = "0.0.0.0:5001"
forwarded_allow_ips = '*'
loglevel = 'DEBUG'

# gunicorn -c gunicorn_config.py app:app -D, #--daemon          Daemonize the Gunicorn process.