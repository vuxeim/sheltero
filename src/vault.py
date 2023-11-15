import os
import datetime

import data


class Vault:

    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.data: data.Data = data.Data()
        self.save_file: str = os.path.join(path, 'saves', self.name, self.name+'.dat')
        self.save_dir = os.path.dirname(self.save_file)
        self.load()

    def load(self) -> None:
        """ Load data to self.data variable """
        if not os.path.exists(self.save_file):
            self.create()
        self.data.load(self.save_file)
        self.data.beg_time = datetime.datetime.now()

    def save(self) -> None:
        """ Saves current vault's data to disk """
        self.data.play_time += datetime.datetime.now() - self.data.beg_time
        self.data.save(self.save_file)

    def create(self) -> None:
        """ Creates a new vault """
        os.mkdir(self.save_dir)
        self.data.zero_init(self.name)
        self.save()
