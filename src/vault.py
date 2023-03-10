import os
import pickle
import datetime

# NOTE Temporary constants because economy and denizens systems aren't implemented yet
STARTING_BALANCE: int = 980
STARTING_DENIZENS: int = 6

class Vault:

    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.save_file: str = os.path.join(path, 'saves', self.name, self.name+'.dat')
        self.save_dir = os.path.dirname(self.save_file)
        self.load()
    
    def load(self) -> None:
        if not os.path.exists(self.save_file):
            self.create(self.name)
        with open(self.save_file, 'rb') as f:
            # TODO make 'self.data' an object of separate class
            self.data = pickle.load(f)
        self.data['beg_time'] = datetime.datetime.now()

    def save(self) -> None:
        """ Saves current vault's data to the disk """
        self.data['play_time'] += datetime.datetime.now() - self.data['beg_time']
        with open(self.save_file, 'wb') as f:
            pickle.dump(self.data, f)

    def create(self) -> None:
        """ Creates a new vault """
        os.mkdir(self.save_dir)
        creation_date = datetime.datetime.now()
        self.data = {
            'name': self.name,
            'creation_date': creation_date,
            'beg_time': creation_date,
            'balance': STARTING_BALANCE,
            'play_time': datetime.timedelta(0),
            'denizens': STARTING_DENIZENS,
        }
        self.save()