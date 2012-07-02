#!/usr/bin/env python
import os
import sys
import json
from subprocess import Popen, PIPE

def log(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()

def find_latest(index_dir):
    res = {}
    for pkg in os.listdir(index_dir):
        pkg_dir = os.path.join(index_dir, pkg)
        if not os.path.isdir(pkg_dir):
            continue
        latest = max(os.listdir(pkg_dir))
        res[pkg] = os.path.join(pkg_dir, latest, pkg + '.cabal')
    return res

def parse_depgraph(pkgs):
    res = {}
    for i, (pkg, cabal) in enumerate(pkgs.iteritems()):
        log('\rParsing %d of %d files...' % (i+1, len(pkgs)))
        p = Popen('./depparse', shell=True, stdin=PIPE, stdout=PIPE)
        result = p.communicate(open(cabal).read())[0]
        res[pkg] = json.loads(result)
    log('done.\n')
    return res

if __name__ == '__main__':
    pkgs = find_latest('index')
    graph = parse_depgraph(pkgs)
    with open('depgraph.json', 'w') as f:
        json.dump(graph, f)
