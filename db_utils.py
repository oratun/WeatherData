from db_config import config
from sqlalchemy import create_engine


# config = {
#     'user': 'username',
#     'password': 'pwd',
#     'host': 'ip',
#     'port': 3306,
#     'db': 'test'
# }

engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}'.format(**config))
