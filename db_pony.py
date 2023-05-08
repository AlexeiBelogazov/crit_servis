import pony.orm
import pymysql
from config import *

db = pony.orm.Database()



class User(db.Entity):
    name = pony.orm.Required(str)
    s_code = pony.orm.Required(str)
    passw = pony.orm.Required(str)
    sticker = pony.orm.Optional('Stickerr')

class Stickerr(db.Entity):
    sticker_unique_id = pony.orm.PrimaryKey(str)
    sticker_id = pony.orm.Optional(str)
    user = pony.orm.Set(User)

def init_db():
    db.bind(provider='mysql', host=HOST, user=USER, passwd=PASSWORD, db=DB_LOGIN)
    db.generate_mapping(create_tables=True)
    with pony.orm.db_session:
       if Stickerr["1"] == None:
           s_none = Stickerr(sticker_unique_id="1", sticker_id=" ")
           pony.orm.commit()



