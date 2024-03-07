# from gevent import monkey
# monkey.patch_socket()
# import logging

# import gevent
# from gevent.queue import Queue
# import pymysql as db

# logging.basicConfig(level=logging.DEBUG)
# LOGGER = logging.getLogger("connection_pool")


# class ConnectionPool:
#     def __init__(self, db_config, time_to_sleep=30, test_run=False):
#         self.username = db_config.get('user')
#         self.password = db_config.get('password')
#         self.host = db_config.get('host')
#         self.port = int(db_config.get('port'))
#         self.max_pool_size = 20
#         self.test_run = test_run
#         self.pool = None
#         self.time_to_sleep = time_to_sleep
#         self._initialize_pool()

#     def get_initialized_connection_pool(self):
#         return self.pool

#     def _initialize_pool(self):
#         self.pool = Queue(maxsize=self.max_pool_size)
#         current_pool_size = self.pool.qsize()
#         if current_pool_size < self.max_pool_size:  # this is a redundant check, can be removed
#             for _ in range(0, self.max_pool_size - current_pool_size):
#                 try:
#                     conn = db.connect(host=self.host,
#                                       user=self.username,
#                                       passwd=self.password,
#                                       port=self.port)
#                     self.pool.put_nowait(conn)

#                 except db.OperationalError as e:
#                     LOGGER.error("Cannot initialize connection pool - retrying in {} seconds".format(self.time_to_sleep))
#                     LOGGER.exception(e)
#                     break
#         self._check_for_connection_loss()

#     def _re_initialize_pool(self):
#         gevent.sleep(self.time_to_sleep)
#         self._initialize_pool()

#     def _check_for_connection_loss(self):
#         while True:
#             conn = None
#             if self.pool.qsize() > 0:
#                 conn = self.pool.get()

#             if not self._ping(conn):
#                 if self.test_run:
#                     self.port = 3306

#                 self._re_initialize_pool()

#             else:
#                 self.pool.put_nowait(conn)

#             if self.test_run:
#                 break
#             gevent.sleep(self.time_to_sleep)

#     def _ping(self, conn):
#         try:
#             if conn is None:
#                 conn = db.connect(host=self.host,
#                                   user=self.username,
#                                   passwd=self.password,
#                                   port=self.port)
#             cursor = conn.cursor()
#             cursor.execute('select 1;')
#             LOGGER.debug(cursor.fetchall())
#             return True

#         except db.OperationalError as e:
#             LOGGER.warn('Cannot connect to mysql - retrying in {} seconds'.format(self.time_to_sleep))
#             LOGGER.exception(e)
#             return False


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

class ConnectionPool:
    def __init__(self, db_config, time_to_sleep=30, test_run=False):
        self.username = db_config.get('user')
        self.password = db_config.get('password')
        self.host = db_config.get('host')
        self.port = int(db_config.get('port'))
        self.max_pool_size = 20
        self.test_run = test_run
        self.time_to_sleep = time_to_sleep
        self._initialize_pool()

    def get_initialized_connection_pool(self):
        return self.Session

    def _initialize_pool(self):
        self.engine = create_engine(f'mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/your_database',
                                    poolclass=QueuePool,
                                    pool_size=self.max_pool_size,
                                    max_overflow=0)
        self.Session = scoped_session(sessionmaker(bind=self.engine))