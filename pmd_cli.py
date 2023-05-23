import sys
import argparse
from pmd_const import *

parse_result = {
  'status': PMD_UNKNOWN,
  'args': None,
  'subcmd': '',
  'matching_subcommands': [],
}

def matching_subcommands(subcommands, cmd):
  matching_subcmds = []
  for sc in subcommands:
    if sc.startswith(cmd):
      matching_subcmds.append(sc)
  
  return matching_subcmds

################################################################################

def prep_cli_parsers():
  subcommands = []
  # Root command line parser
  clparser = argparse.ArgumentParser(prog=PMD_PROGRAM,
                                     description="List available modules and extract their docstring documentation",
                                     epilog="Enjoy using %(prog)s :-)",
                                     exit_on_error=False)
  clparser.add_argument('--version', '-v', version='%(prog)s ' + PMD_VERSION, action='version')

  # Subparser
  subparsers = clparser.add_subparsers(title="Subcommands", help='Subcommands', dest='subcommand');

  # List parser
  lsparser = subparsers.add_parser('list', help='List available modules and/or their properties')
  recursion = lsparser.add_argument_group("Recursion")
  recursion.add_argument('-r', '--recursive', help='Recursively look for modules inside packages', 
                         action='store_true')
  recursion.add_argument('-d', '--max-depth', help='Maximum depth to go down recursively', type=int, default=0)
  properties = lsparser.add_argument_group('Properties')
  properties.add_argument('-n', '--name', help='Print the name property', action='store_true', default=True)
  properties.add_argument('-i', '--ispkg', help='Print the ispkg property', action='store_true', default=False)
  properties.add_argument('-p', '--path', help='Print the path (origin) of the module', action='store_true', default=False)
  lsparser.add_argument('-P', '--paths', help='List only module(s) in the designated path(s)', action='store', nargs='+', default=[])
  print_fmt = properties.add_mutually_exclusive_group()
  print_fmt.add_argument('-t', '--tabular', help='Print information in a tabular format', action='store_true', default=True)
  print_fmt.add_argument('-s', '--sequential', help='Print information in a sequential format', action='store_true', default=False)
  properties.add_argument('-H', '--no-header', help='Do not print the header bar', action='store_true', default=False)
  subcommands.append('list')

  # Extract parser
  exparser = subparsers.add_parser('extract', help='Extract docstring documentation from designated modules')
  exparser.add_argument('-m', '--modules', help='Extract docstring documentation from designated modules',
                        action='store', nargs='+')
  subcommands.append('extract')

  return clparser, subcommands

################################################################################

def parse_cli():
  clparser, subcommands = prep_cli_parsers()
  
  try:
    parse_result['args'] = clparser.parse_args()
    parse_result['status'] = PMD_OK
    parse_result['subcmd'] = parse_result['args'].subcommand
  except argparse.ArgumentError as ae:
    # while loop is used only to be able to break out of conditional statements. It runs only once anyway
    while True:
      if ae.argument_name == 'subcommand':
        # Handle subcommand abbreviations
        q0 = ae.message.find("'")
        q1 = -1
        if q0 == -1:
          break
        if q0 + 1 < len(ae.message):
          q1 = ae.message.find("'", q0 + 1)
        if q1 == -1:
          break
        
        parse_result['subcmd'] = ae.message[q0 + 1:q1]
        parse_result['matching_subcmds'] = matching_subcommands(subcommands, parse_result['subcmd'])
        if len(parse_result['matching_subcmds']) == 0:
          parse_result['status'] = PMD_SUBCMD_INVALID
        elif len(parse_result['matching_subcmds']) == 1:
          sys.argv[1] = parse_result['matching_subcmds'][0]
          parse_cli()
        else:
          parse_result['status'] = PMD_SUBCMD_AMBIGUITY
      else:
        # Exception was thrown due to something other than subcommands
        raise sys.exc_info()
      
      break

################################################################################

def print_parse_errors():
  if parse_result['status'] == PMD_SUBCMD_INVALID:
    print(f"Invalid subcommand '{parse_result['subcmd']}'.")
    print(f"Please use '{PMD_PROGRAM} --help' for usage information.")
  elif parse_result['status'] == PMD_SUBCMD_AMBIGUITY:
    print(f"Ambiguous subcommand '{parse_result['subcmd']}'")
    print('Matching subcommands:')
    for sc in parse_result['matching_subcommands']:
      print(f"\t{sc}")
