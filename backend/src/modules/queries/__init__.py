from src.modules.queries.utils.DatabaseManagerFactory import DatabaseManagerFactory
from src.modules.queries.utils.DatabaseType import DatabaseType
from src.modules.queries.utils.MySQLManager import MySQLManager
from src.modules.queries.utils.PostgreSQLManager import PostgreSQLManager

DatabaseManagerFactory.register(DatabaseType.POSTGRESQL, PostgreSQLManager)
DatabaseManagerFactory.register(DatabaseType.MYSQL, MySQLManager)
