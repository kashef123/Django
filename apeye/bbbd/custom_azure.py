from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = 'kashefappeye'
    account_key = '7ZNKRwMbhi1kkDx4+5s5UBhlF0aun4M377RkquCwtkTBgWWf0dreG+mmfohfLx0zROU4Kc6q8dL+cglTO+bpxg=='
    azure_container = 'media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = 'kashefappeye'
    account_key = '7ZNKRwMbhi1kkDx4+5s5UBhlF0aun4M377RkquCwtkTBgWWf0dreG+mmfohfLx0zROU4Kc6q8dL+cglTO+bpxg=='
    azure_container = 'static'
    expiration_secs = None
