from .mongodb import MONGODB_SETTINGS, MongodbService, MongodbSignature
from .mysql import MYSQL_SETTINGS, MysqlService, MysqlSignature

mongodb_service = (
    MongodbSignature()
    if any(value is None for value in MONGODB_SETTINGS.dict().values())
    else MongodbService()
)

mysql_service = (
    MysqlSignature()
    if any(value is None for value in MYSQL_SETTINGS.dict().values())
    else MysqlService()
)
