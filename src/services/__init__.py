from .mongodb import MongodbService
from .mysql import MYSQL_SETTINGS, MysqlService, MysqlSignature

mongodb_handler = MongodbService()

mysql_service = (
    MysqlSignature
    if any(value is None for value in MYSQL_SETTINGS.dict().values())
    else MysqlService()
)
