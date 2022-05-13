
from storages.backends.azure_storage import AzureStorage
from .settings import AZURE_BLOB_KEY, AZURE_ACCOUNT_NAME

class AzureMediaStorage(AzureStorage):
    account_name = AZURE_ACCOUNT_NAME
    account_key = AZURE_BLOB_KEY
    azure_container = 'media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = AZURE_ACCOUNT_NAME
    account_key = AZURE_BLOB_KEY
    azure_container = 'static'
    expiration_secs = None