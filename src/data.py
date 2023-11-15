import datetime
import pickle
from typing import Any

import utils

# NOTE Temporary constants because economy and denizens systems aren't implemented yet
_STARTING_BALANCE: int = 980
_STARTING_DENIZENS: int = 6


class Data:

    __slots__ = ("name", "creation_date", "beg_time", "balance", "play_time", "denizens")

    name: str
    creation_date: datetime.datetime
    beg_time: datetime.datetime
    balance: int
    play_time: datetime.timedelta
    denizens: int

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
        _default_values = (name, _now, _now, _STARTING_BALANCE, datetime.timedelta(0), _STARTING_DENIZENS)
        if len(self.__slots__) != len(_default_values):
            raise Exception("Not every field has default value asigned")
        _data = {k: v for k, v in zip(self.__slots__, _default_values)}
        self.populate(_data)

    def populate(self, data: dict[str, Any]) -> None:
        """ Set every field to corresponding value """
        for name, value in data.items():
            self._setattr(name, value)

    def _serialize(self) -> dict[str, Any]:
        """ Serialize every file to a dict """
        return {slot: self._getattr(slot) for slot in self.__slots__}
