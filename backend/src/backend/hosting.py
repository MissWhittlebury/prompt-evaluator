from lagom import Container, dependency_definition
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker

container = Container()


DB_URL = "postgresql+psycopg2://postgres:postgres@localhost/prompt_evaluator"


@dependency_definition(container, singleton=True)
def _(c: Container) -> Engine:
    return create_engine(
        url=DB_URL, execution_options={"isolation_level": "AUTOCOMMIT"}
    )


@dependency_definition(container, singleton=True)
def _(c: Container) -> Session:
    return sessionmaker(bind=c[Engine])
    return c[Engine].connect()
