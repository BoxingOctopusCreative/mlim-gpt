import multiprocessing
import os
from dotenv import load_dotenv, find_dotenv

# Tell our app where to get its environment variables from
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
try:
    load_dotenv(dotenv_path)
except IOError:
    find_dotenv()

listen          = os.environ.get('LISTEN')
port            = os.environ.get('PORT')
bind            = f'{listen}:{port}'
reload          = True
#worker_tmp_dir  = '/dev/shm'
workers         = multiprocessing.cpu_count() * 2 + 1
threads         = 4
worker_class    = 'gthread'
accesslog       = './log/gunicorn.access.log'
errorlog        = './log/gunicorn.error.log'
log_level       = 'info'
pid_file        = './run/gunicorn.pid'