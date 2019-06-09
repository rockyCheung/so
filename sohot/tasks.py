from sohot import app
import logging
from sohot.db_orm import addTalkHistory,add_address


@app.task
def write_db(messageDict):
    try:
        address = add_address(nickname=messageDict['nickname'],
                              inetip=messageDict['remote_ip'],
                              port=messageDict['remote_port'])
        talk = addTalkHistory(nickname=messageDict['nickname'],
                              fingure=address.fingure,
                              message=messageDict['sms'],
                              aspect=1,
                              inetip=messageDict['remote_ip'],
                              port=messageDict['remote_port'],
                              broadcast=messageDict['broadcast'])
        logging.info('task write the talk history: %s',talk)
    except Exception as e:
        logging.error(e)