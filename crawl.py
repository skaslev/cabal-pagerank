#!/usr/bin/env python
import sys
import json
import tarfile
from subprocess import Popen, PIPE

def make_tree(filename, verbose=False):
    f = tarfile.open(filename)
    names = f.getnames()
    total = len(names)
    res = {}
    for i, name in enumerate(names):
        if verbose:
            print '\rReading %d of %d files...' % (i+1, total),
            sys.stdout.flush()
        if not name.endswith('.cabal'):
            continue
        pkg, ver, _ = name.split('/')
        res.setdefault(pkg, {})[ver] = f.extractfile(name)
    if verbose:
        print 'done.'
    return res

def get_latest(tree):
    res = {}
    for pkg in tree:
        latest = max(tree[pkg].keys())
        res[pkg] = tree[pkg][latest]
    return res

def parse_depgraph(pkgs, verbose=False):
    res = {}
    total = len(pkgs)
    for i, (pkg, f) in enumerate(pkgs.iteritems()):
        if verbose:
            print '\rParsing %d of %d files...' % (i+1, total),
            sys.stdout.flush()
        p = Popen('./depparse', shell=True, stdin=PIPE, stdout=PIPE)
        result = p.communicate(f.read())[0]
        res[pkg] = json.loads(result)
    if verbose:
        print 'done.'
    return res

if __name__ == '__main__':
    tree = make_tree('00-index.tar.gz', verbose=True)
    pkgs = get_latest(tree)
    graph = parse_depgraph(pkgs, verbose=True)
    with open('depgraph.json', 'w') as f:
        json.dump(graph, f)
