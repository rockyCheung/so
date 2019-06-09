#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey,Sequence,DateTime,func
from sqlalchemy.orm import relationship
import base64
import hashlib
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence
from sohot import Base,Session
import logging

# ***************************************************
# 用户信息表：当前用户个人化信息，除fingure外均由conf中获取
# ***************************************************
class SoUser(Base):
    __tablename__ = 'so_user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String)
    sex = Column(String)
    nickname = Column(String,unique=True, nullable=True)
    createdtime = Column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    #status.0 : 异常 status.1 : 正常
    status = Column(Integer,server_default='1')
    email = Column(String)
    mobile = Column(String)
    idcard = Column(String)
    fingure = Column(String,unique=True, nullable=True)
    # address = relationship("Address", back_populates = "user")#Address代表关联表class名称、user是在变量表class定义中变量名称
    def __repr__(self):
        return "<SoUser(ID='%d',name='%s', sex='%s', nickname='%s', createdtime='%s' , status='%d', email='%s', mobile='%s', idcard='%s', fingure='%s')>" % (
            self.id,self.name, self.sex, self.nickname,self.createdtime,self.status,self.email,self.mobile,self.idcard,self.fingure)

# ***************************************************
# 用户地址信息表：包括当前用户的IP地址信息以及所有与当前在线
# 局域网用户信息，会出现重复的情况，
# 但nickname、fingure要保证所有客户端均唯一
# ***************************************************
class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, Sequence('address_id_seq'),primary_key=True)
    # user_id = Column(Integer, ForeignKey('so_user.id'))
    nickname = Column(String,unique=True, nullable=True)
    fingure = Column(String,unique=True, nullable=True)
    inetip = Column(String)#外网IP
    port = Column(Integer)
    updatetime = Column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    # user = relationship("SoUser", back_populates="address")

    def __repr__(self):
        return "<Address(ID='%d', nickname='%s', fingure='%s' , inetip='%s', port='%s', updatetime='%s')>" % (
            self.id, self.nickname, self.fingure,self.inetip,self.port,self.updatetime)

class TalkHistory(Base):
    __tablename__ = 'talk_history'
    id = Column(Integer, Sequence('talkhis_id_seq'), primary_key=True)
    nickname = Column(String)
    fingure = Column(String)
    message = Column(String)
    aspect = Column(Integer)#0 : I say 1 : opponent say
    createdtime = Column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    inetip = Column(String)  # 外网IP
    port = Column(Integer)
    broadcast = Column(String) #1:广播 0:普通消息

def gen_fingure(nickname):
    hash = hashlib.md5()
    hash.update(nickname.encode("utf-8"))
    return base64.b64encode(hash.digest()).decode("utf-8")

def add_souser(name,sex,email,mobile,idcard,nickname):
    ed_user = SoUser(name=name,
                     sex=sex,
                     email=email,
                     mobile=mobile,
                     idcard=idcard,
                     nickname=nickname,
                     fingure=gen_fingure(nickname))
    # Session = sessionmaker()
    # Session.configure(bind=engine)
    sess = Session()
    sess.add(ed_user)
    sess.commit()
    return ed_user

def query_souser(nickname):
    sess = Session()
    user = sess.query(SoUser).filter_by(nickname=nickname).first()
    return user
'''
批量插入address记录，list格式如：
[{
    "fingure": "YUDztpIUXnM/xz3IPNnZKg==",
    "id": 1,
    "inetip": "localhost",
    "nickname": "edsnickname",
    "port": 8080,
    "updatetime": "2019-06-04 05:48:16",
    "user": null,
    "user_id": 1
}]
'''
def add_address_list(list):
    address_list = []
    for address in list:
        address = Address(nickname=address.get('nickname'),
                          fingure=address.get('fingure'),
                          inetip=address.get('inetip'),
                          port=address.get('port'))
        address_list.append(address)
    sess = Session()
    sess.add_all(address_list)
    sess.commit()
    return address_list

def add_address(nickname,inetip,port):
    address = Address(nickname=nickname,
                      fingure=gen_fingure(nickname),
                      inetip=inetip,
                      port=port)
    sess = Session()
    sess.merge(address)
    sess.commit()
    return address

def query_address(nickname):
    sess = Session()
    address = sess.query(Address).filter_by(nickname=nickname).first()
    return address

def query_remote_user_ip_port(nickname):
    address = query_address(nickname)
    return address.inetip,address.port

def addTalkHistory(nickname,fingure,message,aspect,inetip,port,broadcast):
    talk = TalkHistory(nickname=nickname,fingure=fingure,message=message,aspect=aspect,inetip=inetip,port=port,broadcast=broadcast)
    sess = Session()
    sess.add(talk)
    sess.commit()
    return talk