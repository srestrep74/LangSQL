from src.modules.queries.utils.DatabaseType import DatabaseType
from src.modules.queries.utils.PostgreSQLManager import PostgreSQLManager
from src.modules.queries.utils.MySQLManager import MySQLManager
from src.modules.queries.utils.DatabaseManagerFactory import DatabaseManagerFactory

DatabaseManagerFactory.register(DatabaseType.POSTGRESQL, PostgreSQLManager)
DatabaseManagerFactory.register(DatabaseType.MYSQL, MySQLManager)
