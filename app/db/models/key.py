import enum
import sqlalchemy as sa

from app import db


class Key(db.Base):
    __tablename__ = 'keys'

    class Types(enum.Enum):
        INT = enum.auto()
        BOOL = enum.auto()
        FLOAT = enum.auto()

    name = sa.Column(sa.String, primary_key=True)
    _value = sa.Column('value', sa.String)
    coerce = sa.Column(sa.Enum(Types))

    @property
    def value(self):
        value = self._value
        if not self.coerce:
            return value
        if self.coerce == self.Types.INT:
            return int(value)
        if self.coerce == self.Types.FLOAT:
            return float(value)
        if self.coerce == self.Types.BOOL:
            return value and value != "0"

    @value.setter
    def value(self, value):
        self._value = str(value)
