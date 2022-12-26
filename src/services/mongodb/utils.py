from urllib.parse import quote_plus

from .settings import MongodbSettings


def build_host_url(settings: MongodbSettings) -> str | None:
    user = f"{quote_plus(settings.user)}:{quote_plus(settings.password)}"
    host = f"{settings.host}:{settings.port}"

    tls_parameters = (
        ""
        if settings.tls_file is None
        else (
            "tls=true&"
            f"tlsCAFile={settings.tls_file}&"
            "replicaSet=rs0&"
            "readPreference=secondaryPreferred&"
            "retryWrites=false"
        )
    )

    return f"mongodb://" f"{user}@{host}" f"/?{tls_parameters}"
