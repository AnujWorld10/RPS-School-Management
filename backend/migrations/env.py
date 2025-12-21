from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# -------------------------------------------------
# Import Base and MODELS (THIS IS CRITICAL)
# -------------------------------------------------
from app.database.base import Base
import app.models  # noqa: F401  <-- DO NOT REMOVE

# -------------------------------------------------
# Alembic Config
# -------------------------------------------------
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def get_sync_database_url() -> str:
    """
    Convert async DB URL to sync for Alembic.
    Alembic does NOT support async engines.
    """
    url = config.get_main_option("sqlalchemy.url")

    if url.startswith("mysql+asyncmy"):
        url = url.replace("mysql+asyncmy", "mysql+pymysql")

    return url


# -------------------------------------------------
# Offline migrations
# -------------------------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_sync_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------------------------------
# Online migrations
# -------------------------------------------------
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    config.set_main_option("sqlalchemy.url", get_sync_database_url())

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------------------------------
# Entry point
# -------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()