import os
from dataclasses import dataclass, field
from typing import List, Optional

ROOT_PATH = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

TRAINING_DATA_PATH = os.path.join(ROOT_PATH, "training_data")

STATIC_RESOURCE_PATH = os.path.join(ROOT_PATH, "static")

LOGDIR = os.getenv("KIWI_LOG_DIR", os.path.join(ROOT_PATH, "logs"))

current_directory = os.getcwd()

DATA_DIR = os.path.join(ROOT_PATH, "data")


@dataclass
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    log_level: str = field(
        default="INFO",
        metadata={
            "help": "Logging level",
            "valid_values": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        },
    )
    api_keys: List[str] = field(
        default_factory=list,
        metadata={
            "help": "API keys",
        },
    )
    encrypt_key: Optional[str] = field(
        default="your_secret_key",
        metadata={"help": "The key to encrypt the data"},
    )
    host: str = field(default="0.0.0.0", metadata={"help": "Webserver deploy host"})
    port: int = field(
        default=5670, metadata={"help": "Webserver deploy port, default is 5670"}
    )
    database: Optional[str] = field(
        default="duckdb",
        metadata={
            "help":
                "Database connection config, now support SQLite and DuckDB"
        },
    )
    db_ssl_verify: Optional[bool] = field(
        default=False,
        metadata={"help": "Whether to verify the SSL certificate of the  database"},
    )
    default_thread_pool_size: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "The default thread pool size, If None, use default config of python "
                "thread pool"
            )
        },
    )
    remote_embedding: Optional[bool] = field(
        default=False,
        metadata={
            "help": (
                "Whether to enable remote embedding models. If it is True, you need"
                " to start a embedding model through `kiwi start worker --worker_type "
                "text2vec --model_name xxx --model_path xxx`"
            )
        },
    )
    remote_rerank: Optional[bool] = field(
        default=False,
        metadata={
            "help": (
                "Whether to enable remote rerank models. If it is True, you need"
                " to start a rerank model through `kiwi start worker --worker_type "
                "text2vec --rerank --model_name xxx --model_path xxx`"
            )
        },
    )
