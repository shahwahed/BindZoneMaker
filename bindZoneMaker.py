#!/bin/python3
# -*- coding: utf-8 -*-

import yaml
import json
import sys
import datetime
import getopt
from jinja2 import Environment, FileSystemLoader



def main(argv):
    _zonefile = ''
    try:
        opts, args = getopt.getopt(argv, "z:", ["zonefile="])
    except getopt.GetoptError:
        print('bindZoneMaker.py -z <zonefile.json>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('bindZoneMaker.py -z <zonefile.json>')
            sys.exit()
        elif opt in ("-z", "--zonefile"):
            _zonefile = arg
    

    try:
        #dnszonejson = json.loads(open('dns_reverse_example.json').read())
        dnszonejson = json.loads(open(_zonefile).read())

        #create Jinja2 environment object and refer to templates directory
        env = Environment(loader=FileSystemLoader('.'))

        template = env.get_template('zone.j2')

        template.globals['now'] = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        #print(dnszonejson)
        print(template.render(dnszonejson))
    except (OSError) as ex:
        print(ex)
    except:
        print("An unexpected error occurred")
        raise

if __name__ == "__main__":
    main(sys.argv[1:])