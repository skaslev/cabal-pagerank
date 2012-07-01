#!/usr/bin/env python
import sys
import json

if __name__ == '__main__':
    with open('depgraph.json') as f:
        graph = json.load(f)
    pkg = sys.argv[1]
    users = set()
    for n, deps in graph.iteritems():
        if pkg in deps:
            users.add(n)
    print '\n'.join(users)
