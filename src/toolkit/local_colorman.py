import inspect
import runpy


# Workaround that allows to import colorman from
# interactive python shell (python `-i` flag).
#
# Basically, this file mimics being colorman module.


for name, cls in runpy.run_path('./utils/colorman.py').items():
    if inspect.isclass(cls):
        globals().update({name: cls})

del inspect, runpy