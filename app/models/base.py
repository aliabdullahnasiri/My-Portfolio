from datetime import datetime

import humanize
from flask import request
from numerize import numerize
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr

from app.extensions import console, db


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, autoincrement=True)

    # Timestamps
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now(),
        nullable=False,
    )

    @classmethod
    def count(cls):
        return numerize.numerize(cls.query.count(), 2)

    @property
    def display_created_at(self) -> str:
        return (
            self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else "N/A"
        )

    @property
    def display_updated_at(self) -> str:
        return (
            self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else "N/A"
        )

    @property
    def display_natural_created_at(self) -> str:
        return humanize.naturaltime(self.updated_at)

    @property
    def display_natural_updated_at(self) -> str:
        return humanize.naturaltime(self.updated_at)

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.display_created_at,
            "updated_at": self.display_updated_at,
        }


def all(self):
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 100))
        offset = (page - 1) * limit

        return self.offset(offset).limit(abs(limit))
    except Exception as err:
        console.print(err)

    return self


db.Model.query_class.all = all
db.Model = Base
