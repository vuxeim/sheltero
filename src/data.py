import datetime
import pickle
from typing import Any

# NOTE Temporary constants because economy
# and denizens systems aren't implemented yet
_STAR_BALANCE: int = 980
_STAR_DENIZENS: int = 6


class Data:

    __slots__ = ("name", "creation_date", "beg_time", "balance", "play_time", "denizens")

    def __init__(self) -> None:
        self.name: str
        self.creation_date: datetime.datetime
        self.beg_time: datetime.datetime
        self.balance: int
        self.play_time: datetime.timedelta
        self.denizens: int

    def _setattr(self, name: str, obj: Any) -> None:
        """
        Sets field to an object if field exists.
        Raises AttributeError otherwise.
        """
        if name not in self.__slots__:
            raise AttributeError(f"Unknown field {name}")
        setattr(self, name, obj)

    def _getattr(self, name: str) -> Any:
        """
        Return object corresponding to field's name.
        Raises AttributeError if field's name doesn't exist.
        """
        try:
            return getattr(self, name)
        except AttributeError as err:
            err.add_note(f"Unknown field {name}")
            raise err

    def load(self, file: str) -> None:
        """ Read data from disk then serialize and populate """
        with open(file, 'rb') as f:
            _data = pickle.load(f)
            self.populate(_data)

    def save(self, file: str) -> None:
        """ Serialize and save all data fields to disk """
        with open(file, 'wb') as f:
            data = self._serialize()
            pickle.dump(data, f)

    def zero_init(self, name: str) -> None:
        """ Populate fields with default values """
        _now = datetime.datetime.now()
        _default_values = (name, _now, _now, _STAR_BALANCE, datetime.timedelta(0), _STAR_DENIZENS)
        _data = dict(zip(self.__slots__, _default_values, strict=True))
        self.populate(_data)

    def populate(self, data: dict[str, Any]) -> None:
        """ Set every field to corresponding value """
        for name, value in data.items():
            self._setattr(name, value)

    def _serialize(self) -> dict[str, Any]:
        """ Serialize every file to a dict """
        return {slot: self._getattr(slot) for slot in self.__slots__}
