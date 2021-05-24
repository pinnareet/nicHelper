# AUTOGENERATED! DO NOT EDIT! File to edit: datetime.ipynb (unless otherwise specified).

__all__ = ['datestamp', 'stringToTimestamp']

# Cell
from beartype import beartype

# Cell
from datetime import datetime, timezone
@beartype
def datestamp(dt:datetime = datetime.utcnow())->int:
  datestamp = datetime(day=dt.day,month=dt.month,year=dt.year,tzinfo=timezone.utc).timestamp()
  return int(datestamp)

# Cell
@beartype
def stringToTimestamp(stringTime:str, formatString:str, timeZone:timezone = timezone.utc)->float:
  return datetime.strptime(stringTime,formatString).replace(tzinfo=timeZone).timestamp()