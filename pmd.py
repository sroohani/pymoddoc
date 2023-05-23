#! /usr/bin/env python3

import os
import pydoc
from pmd_cli import parse_result, parse_cli, print_parse_errors
from pmd_const import *
from pmd_subcmd import mod_info, subcommand_handlers

# def handle_cmd_list(mods, args):
#   nArgs = len(args)
#   name = ispkg = False
#   if nArgs == 0 or args[0] == 'all':
#     name = ispkg = True
#   else:
#     name = args[0] == 'name'
#     ispkg = args[0] == 'ispkg'
#   sep = ' ' if name and ispkg else ''

#   for m in mods:
#     print(f"{m.name if name else ''}{sep}{m.ispkg if ispkg else ''}")

# def module_exists_in(mods, mod):
#   for m in mods:
#     if m.name == mod:
#       return True

#   return False

# def handle_cmd_gen(mods, args):
#   nArgs = len(args)
#   if nArgs < 1:
#     return
  
#   pager = os.environ.get("PAGER", "")
#   os.environ["PAGER"] = "cat"

#   for a in args:
#     print(f"======== {a} ========\n")
#     if module_exists_in(mods, a):
#       doc = str(pydoc.doc(a))
#       if doc.endswith("None"):
#         doc = doc[:-4]
#       print(doc)
#     else:
#       print("Module not found\n")
  
#   os.environ["PAGER"] = pager


def main():
  parse_cli()
  if parse_result['status'] != PMD_OK:
    print_parse_errors()
    exit(-1)

  if parse_result['subcmd'] in subcommand_handlers:
    subcommand_handlers[parse_result['subcmd']]()

################################################################################

if __name__ == "__main__":
  main()
