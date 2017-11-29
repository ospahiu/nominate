DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
DATABASE_NAME = 'nominate.db'
SECRET_KEY = 'secret key'
SESSION_TYPE = 'filesystem'
CELERY_BROKER_URL = 'redis://localhost:6379',
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
