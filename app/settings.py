from typing import Any, Dict, List, Union, Optional

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = None  # Set from pyproject.toml
    PROJECT_SLUG: str = None  # Set from pyproject.toml

    HTTP_HOST: AnyHttpUrl = 'http://0.0.0.0'
    HTTP_PORT: int = 8000
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    API_ROOT: str = ''
    DEBUG: bool = False

    CONVERTER_TYPE: str = 'apilayer'

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = False
        env_file = '.env'

    def __init__(self, *args, **kwargs):
        import pathlib
        import tomlkit

        super().__init__(*args, **kwargs)

        cwd = pathlib.Path(__file__).parent.parent.absolute()
        pyproject_toml_path = cwd / 'pyproject.toml'

        if pyproject_toml_path.exists():
            with open(str(pyproject_toml_path)) as f:
                pyproject_toml = tomlkit.parse(string=f.read())

            if 'tool' in pyproject_toml and 'poetry' in pyproject_toml['tool']:
                self.PROJECT_SLUG = pyproject_toml['tool']['poetry']['name']
                self.PROJECT_NAME = pyproject_toml['tool']['poetry']['description']

