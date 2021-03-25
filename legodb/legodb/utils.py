import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


def load_secret(name, path='/var/openfaas/secrets/'):
    filepath = os.path.join(path, name)
    with open(filepath) as f:
        secret = f.read().rstrip('\n')
    return secret


def create_database_session():
    engine = database_engine_from_secrets()
    session = database_session(engine)
    return session


def database_engine_from_secrets():
    url = database_url_from_secrets()
    engine = database_engine(url)
    return engine


def database_url_from_secrets():
    host = load_secret('database-host')
    user = load_secret('database-user')
    password = load_secret('database-password')
    schema = os.environ.get('database-name', 'openfaasdb')
    port = int(os.environ.get('database-port', '3306'))
    url = database_url(host, port, user, password, schema)
    return url


def database_engine(url):
    engine = create_engine(url)
    return engine


def database_session(engine):
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()
    return session


def database_url(host, port, user, password, schema):
    url = f"mariadb+mariadbconnector://{user}:{password}@{host}:{port}/{schema}?charset=utf8mb4"
    return url
