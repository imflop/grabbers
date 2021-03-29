from dependency_injector import containers
from dependency_injector.providers import Configuration, Factory

from .services import HHService


class Container(containers.DeclarativeContainer):

    config = Configuration()
    hh_service = Factory(HHService)
