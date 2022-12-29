from urllib.parse import quote_plus

from .settings import StrictMongodbSettings


def build_host_url(settings: StrictMongodbSettings) -> str:
    return (
        f"mongodb://"
        f"{quote_plus(settings.user)}:"
        f"{quote_plus(settings.password)}@"
        f"{settings.host}:"
        f"{settings.port}"
    ) + (
        ""
        if settings.tls_file is None
        else (
            f"/?"
            f"tls=true&"
            f"tlsCAFile={settings.tls_file}&"
            f"replicaSet=rs0&"
            f"readPreference=secondaryPreferred&"
            f"retryWrites=false"
        )
    )
