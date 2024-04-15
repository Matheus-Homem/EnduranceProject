import os

class Mapper:
    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, name):
        return Mapper(os.path.join(self._path, name))

    def __call__(self):
        return self._path