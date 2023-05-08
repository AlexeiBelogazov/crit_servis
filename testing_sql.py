import unittest
from db_pony import *
from config import *


init_db()
class TestDBConnection(unittest.TestCase):
    def test_db_connection(self):

        self.assertIsNotNone(db)

    def test_create_user(self):
        with pony.orm.db_session:
            user = User(name='Test User', s_code='123', passw='password', sticker="1")
            pony.orm.commit()
            self.assertIsNotNone(user.id)

    def test_create_stickerr(self):
        with pony.orm.db_session:
            stickerr = Stickerr(sticker_unique_id='123', sticker_id='456')
            pony.orm.commit()
            self.assertIsNotNone(stickerr.sticker_unique_id)

    def test_update_user(self):
        with pony.orm.db_session:
            user = User[7]
            user.s_code = '789'
            pony.orm.commit()
            updated_user = User[7]
            self.assertEqual(updated_user.s_code, '789')

    def test_update_stickerr(self):
        with pony.orm.db_session:
            stickerr = Stickerr["12"]
            stickerr.sticker_id = '789'
            pony.orm.commit()
            updated_stickerr = Stickerr["12"]
            self.assertEqual(updated_stickerr.sticker_id, '789')

    def test_delete_user(self):
        with pony.orm.db_session:
            user = User.get(name='Test User')
            user.delete()
            pony.orm.commit()
            deleted_user = User.get(name='Test User')
            self.assertIsNone(deleted_user)

    def test_delete_stickerr(self):
        with pony.orm.db_session:
            stickerr = Stickerr.get(sticker_unique_id='123')
            stickerr.delete()
            pony.orm.commit()
            deleted_stickerr = Stickerr.get(sticker_unique_id='123')
            self.assertIsNone(deleted_stickerr)

    def test_get_user(self):
        with pony.orm.db_session:
            user = User(name='Test User', s_code='123', passw='password',sticker="1")
            pony.orm.commit()
            retrieved_user = User.get(name='Test User')
            self.assertIsNotNone(retrieved_user)

if __name__ == '__main__':
    unittest.main()
