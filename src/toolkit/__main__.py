import inspect

# This file is responsible for importing names from __init__
# You should edit tools in the __init__.py file

try:
    _tk = __import__('__init__', globals(), locals())
except ModuleNotFoundError:
    print(f'Correct usage:\npython -i toolkit')
    exit(1)

tools = []
for name, item in inspect.getmembers(_tk):
    if not name.startswith('_') and name not in [module[0] for module in inspect.getmembers(_tk, inspect.ismodule)]:
        if name not in dir(__builtins__) and name not in locals().keys() and name not in globals().keys():
            pair = {name: item}
            locals().update(pair)
            globals().update(pair)
            tools.append([str(type(item))[8:-2], name, item])
        else:
            print(f'ERROR!!! {name!r} already exists in scope')

print('Welcome in sheltero tools!', path())
for tool_type in set([tool[0] for tool in tools]):
    print(tool_type+'s:')
    for item in sorted(tools, key=lambda item: item[0]):
        if item[0] == tool_type:
            print(f'\t{item[1]} - {item[2].__doc__ or ""}')

del _tk, inspect, tools
