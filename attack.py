#!/usr/bin/env python

import argparse
import sys

from stix2 import TAXIICollectionSource, Filter
from taxii2client import Collection


cb_response_data_sources = ['Binary file metadata',
                            'DLL monitoring',
                            'File monitoring',
                            'Loaded DLLs',
                            'Process command-line parameters',
                            'Process monitoring',
                            'Process use of network']

endgame_data_sources = ['Process command-line parameters',
                        'Process monitoring']

crowdstrike_data_sources = ['Process command-line parameters',
                            'Process monitoring']


def data_source_match(data_sources, match_list):
  '''Given a list of data sources from an ATT&CK technique, return True if any
  data source appears in match_list.
  '''
  match = False

  for data_source in data_sources:
    if data_source.lower() in [ds.lower() for ds in match_list]:
      match = True

  return match


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--matrix", type=str, action="store", 
                      default="enterprise",
                      help="Matrix to query (enterprise, mobile, pre)")
  parser.add_argument("--dump-data-sources", action="store_true",
                      help="Dump data sources to data_sources.txt")

  args = parser.parse_args()
 
  args.matrix = args.matrix.lower()
  if args.matrix == 'pre':
    matrix = "062767bd-02d2-4b72-84ba-56caef0f8658"
  elif args.matrix == 'mobile':
    matrix = "2f669986-b40b-4423-b720-4396ca6a462b"
  elif args.matrix == 'enterprise':
    matrix = "95ecc380-afe9-11e4-9b6c-751b66dd541e"

  # Initialize dictionary to hold Enterprise ATT&CK content
  attack = {}

  # Establish TAXII2 Collection instance for Enterprise ATT&CK
  collection = Collection("https://cti-taxii.mitre.org/stix/collections/{0}/"\
    .format(matrix))

  # Supply the collection to TAXIICollection
  tc_source = TAXIICollectionSource(collection)

  # Create filters to retrieve content from Enterprise ATT&CK
  filter_objs = {"techniques": Filter("type", "=", "attack-pattern")}

  # Retrieve all Enterprise ATT&CK content
  for key in filter_objs:
    attack[key] = tc_source.query(filter_objs[key])

  all_techniques = attack["techniques"]

  technique_count = 0
  techniques_without_data_source = 0
  techniques_cb_observable = 0
  data_sources = set()

  for technique in all_techniques:
    technique_count += 1
   
    if 'x_mitre_data_sources' in technique.keys():
      if data_source_match(technique['x_mitre_data_sources'],
                           #TODO: Make the match list a passable argument.
                           match_list=crowdstrike_data_sources) == True:
        techniques_cb_observable += 1
        
      if args.dump_data_sources == True:
        [data_sources.add(data_source) for data_source in technique['x_mitre_data_sources']]

    else:
      techniques_without_data_source += 1

  print('Techniques: {0}'.format(technique_count))
  print('Techniques Observable: {0} ({1}%)'\
    .format(techniques_cb_observable,
            round((techniques_cb_observable / technique_count) * 100)))

  if args.dump_data_sources == True:
    with open('data_sources.txt', 'w') as fh_data_sources:
      data_sources = list(data_sources)
      data_sources.sort()
      for data_source in data_sources:
        fh_data_sources.write('{0}\n'.format(data_source))
    

if __name__ == '__main__':

  main()