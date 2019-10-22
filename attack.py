#!/usr/bin/env python

import argparse
import csv
import sys

from stix2 import TAXIICollectionSource, Filter
from taxii2client import Collection


def data_source_match(data_sources, match_list):
  '''Given a list of data sources from an ATT&CK technique, return True if any
  data source appears in match_list.
  '''
  match = False

  for data_source in data_sources:
    if data_source.lower() in [ds.lower() for ds in match_list]:
      match = True

  return match


def parse_data_source_list(path):
  ret = set()

  with open(path, 'r') as input_file:
    for data_source in input_file.readlines():
      ret.add(data_source.strip().lower())

  return list(ret)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--matrix", type=str, action="store", 
                      default="enterprise",
                      help="Matrix to query (enterprise, mobile, pre)")

  # Tools related to Data Sources
  parser.add_argument("--dump-data-sources", action="store_true",
                      help="Dump data sources to data_sources.txt")
  parser.add_argument("--dump-techniques", action="store_true",
                      help="Dump techniques and data sources to techniques.txt")
  parser.add_argument("--dump-matching-techniques", action="store_true",
                      help="Dump techniques that map to match-data-sources to matching-techniques.txt")
  parser.add_argument("--match-data-sources", type=str, action="store",
                      help="A file containing a list of data sources that to match against techniques.")

  args = parser.parse_args()

  match_data_sources = None
  if args.match_data_sources:
    match_data_sources = parse_data_source_list(args.match_data_sources)

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
  techniques_observable = 0
  techniques_with_data_sources = []
  data_sources = set()
  matching_techniques = set()

  for technique in all_techniques:
    technique_count += 1
    technique_id = technique['external_references'][0]['external_id']
  
    if 'x_mitre_data_sources' in technique.keys():
      if match_data_sources is not None:
        if data_source_match(technique['x_mitre_data_sources'],
                            match_list=match_data_sources) == True:
          techniques_observable += 1

          if args.dump_matching_techniques == True:
            matching_techniques.add(technique_id)

      if args.dump_data_sources == True:
        [data_sources.add(data_source) for data_source in technique['x_mitre_data_sources']]

      if args.dump_techniques == True:
        [techniques_with_data_sources.append((technique_id,data_source)) for data_source in technique['x_mitre_data_sources']]

    else:
      techniques_without_data_source += 1

  if match_data_sources is not None:
    print('Techniques: {0}'.format(technique_count))
    print('Techniques Observable: {0} ({1}%)'\
      .format(techniques_observable,
              round((techniques_observable / technique_count) * 100)))
        
  if args.dump_data_sources == True:
    with open('data_sources.txt', 'w') as fh_data_sources:
      data_sources = list(data_sources)
      data_sources.sort()
      for data_source in data_sources:
        fh_data_sources.write('{0}\n'.format(data_source))

  if args.dump_matching_techniques == True:
    with open('matching_techniques.txt', 'w') as fh_matching_techniques:
      matching_techniques = list(matching_techniques)
      matching_techniques.sort()
      for data_source in matching_techniques:
        fh_matching_techniques.write('{0}\n'.format(data_source))
    
  if args.dump_techniques == True:
    with open('techniques.txt', 'w') as fh_techniques:
      csvwriter = csv.writer(fh_techniques, quoting=csv.QUOTE_ALL)
      csvwriter.writerow(['id', 'data_source'])
      for technique in techniques_with_data_sources:
        csvwriter.writerow(technique)

if __name__ == '__main__':

  main()
