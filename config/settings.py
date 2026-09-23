from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()

os.environ.setdefault("HF_HOME", os.getenv("HF_HOME", ".cache/huggingface"))
os.environ.setdefault("TRANSFORMERS_CACHE", os.environ["HF_HOME"])


@dataclass(frozen=True)
class DatabaseSettings:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass(frozen=True)
class ModelSettings:
    tokenizer_model: str
    embedding_model: str
    hf_home: str



def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "tokenization_db"),
    )


def get_model_settings() -> ModelSettings:
    return ModelSettings(
        tokenizer_model=os.getenv("TOKENIZER_MODEL", "distilbert-base-uncased"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "distilbert-base-uncased"),
        hf_home=os.getenv("HF_HOME", ".cache/huggingface"),
    )

