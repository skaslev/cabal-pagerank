#!/usr/bin/env python
import json

def rank(graph, d=0.85, iterations=10):
    backlinks = {n: [] for n in graph}
    for n in graph:
        for other in graph[n]:
            backlinks.setdefault(other, []).append(n)
    N = len(graph)
    pr = {n: 1.0 / N for n in graph}
    for _ in xrange(iterations):
        new_pr = {}
        for n in graph:
            new_pr[n] = (1.0 - d) / N + d * sum(pr[l] / len(graph[l]) for l in backlinks[n])
        pr = new_pr
    s = sum(pr.itervalues())
    pr = {n: r / s for n, r in pr.iteritems()}
    return pr

if __name__ == '__main__':
    with open('depgraph.json') as f:
        graph = json.load(f)
    pr = rank(graph)
    for i, n in enumerate(sorted(graph.keys(), key=lambda n: pr[n], reverse=True)):
        print '%4d %s %f' % (i+1, n.ljust(40), pr[n])
