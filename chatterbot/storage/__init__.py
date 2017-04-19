from .storage_adapter import StorageAdapter
from .django_storage import DjangoStorageAdapter
from .jsonfile import JsonFileStorageAdapter
from .mongodb import MongoDatabaseAdapter

# FIXME Better way manage import
try:
    from .sqlalchemy_storage import SQLAlchemyDatabaseAdapter
except ImportError:
    pass
