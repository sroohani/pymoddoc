#! /usr/bin/env python3

import sys
import os
import pkgutil
import pydoc

def handle_cmd_list(mods, args):
  nArgs = len(args)
  name = ispkg = False
  if nArgs == 0 or args[0] == 'all':
    name = ispkg = True
  else:
    name = args[0] == 'name'
    ispkg = args[0] == 'ispkg'
  sep = ' ' if name and ispkg else ''

  for m in mods:
    print(f"{m.name if name else ''}{sep}{m.ispkg if ispkg else ''}")

def module_exists_in(mods, mod):
  for m in mods:
    if m.name == mod:
      return True

  return False

def handle_cmd_gen(mods, args):
  nArgs = len(args)
  if nArgs < 1:
    return
  
  pager = os.environ.get("PAGER", "")
  os.environ["PAGER"] = "cat"

  for a in args:
    print(f"======== {a} ========\n")
    if module_exists_in(mods, a):
      doc = str(pydoc.doc(a))
      if doc.endswith("None"):
        doc = doc[:-4]
      print(doc)
    else:
      print("Module not found\n")
  
  os.environ["PAGER"] = pager


cmd_handlers = {
'list': handle_cmd_list,
'gen': handle_cmd_gen,
}

def main():
  mods = list(pkgutil.iter_modules())
  nArgs = len(sys.argv)
  cmd = sys.argv[1] if nArgs > 1 else ''
  args = sys.argv[2:] if nArgs > 2 else []
  
  if cmd in cmd_handlers:
    cmd_handlers[cmd](mods, args)
  else:
    sys.exit(1)
  
if __name__ == "__main__":
  main()
