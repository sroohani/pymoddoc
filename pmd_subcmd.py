import pkgutil
import os
import importlib
import sys
from pmd_cli import parse_result

mod_info = []
depth = 1

def basic_module_info(modpath):
  path = os.path.abspath(modpath)
  if os.path.exists(path):
    parts = [part for part in path.split("/") if len(part)]
    modname = parts[-1]
    if modname.endswith(".py"):
      parts[-1] = modname = modname[:-3]

    for p in parts[:-1][::-1]:
      try:
        m = importlib.import_module(modname)
        del sys.modules[modname]
        del m
        if os.path.isdir(path):
          return modname, True, True
        else:
          return modname, True, False
      except ModuleNotFoundError as mnfe:
        modname = p + '.' + modname
        print(modname)
        continue
        
    return None, False, False
  else:
    return None, False, False

################################################################################

def list_modules(mods, parent = ''):
  global depth
  for m in mods:
    mi = {'name': (parent + '.' if len(parent) else '') + m.name, 'ispkg': m.ispkg}
    ms = m.module_finder.find_spec(m.name)
    mi['has_location'] = ms.has_location
    mi['path'] = os.path.dirname(ms.origin) if ms.has_location else ''

    mod_info.append(mi)

    if m.ispkg and ms.has_location and parse_result['args'].recursive:
      if parse_result['args'].max_depth > 0:
        if depth < parse_result['args'].max_depth:
          depth += 1
          list_modules(list(pkgutil.iter_modules([mi['path']])), mi['name'])
          depth -= 1
      else:
        list_modules(list(pkgutil.iter_modules([mi['path']])), mi['name'])

################################################################################

def calc_max_col_widths(widths):
  for mi in mod_info:
    if len(mi['name']) > widths['name']:
      widths['name'] = len(mi['name'])
    if parse_result['args'].path and len(mi['path']) > widths['path']:
      widths['path'] = len(mi['path'])

################################################################################

def handle_list():
  if parse_result['args'].paths:
    for path in parse_result['args'].paths:
      (hierarchy, isvalid, _) = basic_module_info(path)
      if isvalid:
        if (lastindex := hierarchy.rfind('.')) == -1:
          lastindex = len(hierarchy)
        list_modules(list(pkgutil.iter_modules([path])), hierarchy[:lastindex])
  else:
    list_modules(list(pkgutil.iter_modules()))
  
  widths = {'name': 0, 'path': 0}
  calc_max_col_widths(widths)
  
  for m in mod_info:
    print(m['name'])

################################################################################

def handle_extract():
  print("handle_extract")

################################################################################

subcommand_handlers = {
'list': handle_list,
'extract': handle_extract,
}
