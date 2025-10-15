import pymysql
pymysql.version_info = (1, 4, 0, "final", 0)   # spoof higher version
pymysql.install_as_MySQLdb()
