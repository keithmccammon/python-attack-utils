# Python ATT&CK Utils

## Purpose

I wrote this to solve my problems, not to solve all problems for everyone. If you want a much more full-featured Python client for ATT&CK, see https://github.com/Cyb3rWard0g/ATTACK-Python-Client. 

At present, the focus is on analysis of data sources as they relate to techniques.

Feedback welcome.

## Setup (using virtualenv)
```bash
mkvirtualenv -p<PATH_TO_PYTHON3> python-attack-utils

python setup.py develop
```

## Usage

To dump a list of all data sources associated with ATT&CK techniques (NOTE: A list of data sources is provided in data\data_sources.txt):

```bash
./attack.py --dump-data-sources
```

To measure the number of techniques that are observable based on a list of data sources (NOTE: Sample lists for some endpoint product types are provided in the data directory):

1. Create an input file containing one data source per line.

2. Get matches!

```bash
./attack.py --match-data-sources data/edr_generic_data_sources.txt
```
