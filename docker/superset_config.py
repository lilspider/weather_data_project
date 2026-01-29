import os

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SUPERSET_SQLALCHEMY_DATABASE_URI',
    'postgresql+psycopg2://superset_user:superset_password@postgres/superset_db'
)
