from settings import db_config
from sqlalchemy import create_engine


# config = {
#     'user': 'username',
#     'password': 'pwd',
#     'host': 'ip',
#     'port': 3306,
#     'db': 'test'
# }
sa_url = 'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}'.format(**db_config)
engine = create_engine(sa_url)