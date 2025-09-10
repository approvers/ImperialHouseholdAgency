from pydantic_settings import BaseSettings

from src.domain.config import DomainConfigIF


class ImperialHouseholdAgencyConfig(DomainConfigIF, BaseSettings):
    pass
