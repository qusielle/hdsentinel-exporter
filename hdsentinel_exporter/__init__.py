import pydantic


class Settings(pydantic.BaseSettings):
    debug: bool = pydantic.Field(False)
    host: str = pydantic.Field('localhost')
    port: int = pydantic.Field(61220)
    exporter_port: int = pydantic.Field(9958)
    interval: int = pydantic.Field(10)

    class Config:
        env_prefix = 'hds_exp_'


settings = Settings()
