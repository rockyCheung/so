from sohot.db_orm import SoUser,add_souser,query_souser,add_address,Address
import logging
from sohot import Base,engine
import sys

def test_db_init():
    Base.metadata.create_all(engine)


def test_add_souser():
    sss = add_souser(name='ed', sex='1', email='123@qq.com', mobile='12399999999', idcard='11111111111',
                     nickname='edsnickname')
    return sss

def test_query_souser():
    ll = query_souser('edsnickname')
    # assert 0,ll
    logging.debug("@@@@@@@@@@@@@@",ll)
    logging.info("@@@@@@@@@@@@@@", ll)

def test_add_address():
    ll = query_souser('edsnickname')

    add_address(user_id=ll.id, nickname='edsnickname', fingure=ll.fingure, hostname='localhost', inetip='127.0.0.1', port='8080')

if __name__ == '__main__':
    # test_db_init()
    # test_add_souser()
    pass
