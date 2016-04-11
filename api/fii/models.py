# -*- coding: utf-8 -*-

from sqlalchemy import (Table, Column, BigInteger, Text, DateTime, ForeignKey,
                        Boolean)
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseORM(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def dict(self):
        retval = {}
        klasses = list(self.__class__.__mro__)
        klasses.reverse()
        for klass in klasses:
            for attr in klass.__dict__:
                if isinstance(getattr(klass, attr), InstrumentedAttribute):
                    # Only allow JSON serializable values
                    value = getattr(self, attr)
                    if type(value) in [unicode, str, int, float]:
                        retval[attr] = getattr(self, attr)
        return retval

    @classmethod
    def get_or_create(cls, store, query, **kwargs):
        # Auto assign query parameters when creating/updating
        kwargs.update(query)

        obj = store.query(cls).filter_by(**query).first()
        if obj is not None:
            for key, value in kwargs.iteritems():
                setattr(obj, key, value)
            return obj, False
        obj = cls(**kwargs)
        store.add(obj)
        return obj, True


watcher_fii_map = Table('watcher_fii_map', Base.metadata,
                        Column('watcher_id', BigInteger,
                               ForeignKey('watcher.id')),
                        Column('fii_code', Text,
                               ForeignKey('fii.code')))


class FII(BaseORM):
    __tablename__ = 'fii'

    code = Column(Text, primary_key=True)
    company = Column(Text)
    fund = Column(Text)
    type = Column(Text)
    url = Column(Text)

    error = Column(Boolean, default=False)

    logs = relationship("FIILog", back_populates="fii")
    watchers = relationship("Watcher",
                            secondary=watcher_fii_map,
                            back_populates="fiis")


class Watcher(BaseORM):
    __tablename__ = 'watcher'

    (STATUS_ADMIN,
     STATUS_USER_FREE,
     STATUS_USER_LIMITED,
     STATUS_INACTIVE) = (
        'admin',
        'user_free',
        'user_limited',
        'inactive',
    )

    id = Column(BigInteger, primary_key=True)
    email = Column(Text)
    status = Column(Text, default=STATUS_USER_LIMITED)

    fiis = relationship("FII",
                        secondary=watcher_fii_map,
                        back_populates="watchers")


class FIILog(BaseORM):
    __tablename__ = 'fii_log'

    id = Column(BigInteger, primary_key=True)

    fii_code = Column(Text, ForeignKey('fii.code'))
    fii = relationship("FII", back_populates="logs")

    html = Column(Text)
    subject = Column(Text)
    link = Column(Text)
    notification_date = Column(DateTime)
