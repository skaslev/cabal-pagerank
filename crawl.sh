#!/bin/sh
echo "Cleaning..."
rm depparse 00-index.tar.gz depgraph.json

echo "Downloading index..."
curl -O http://hackage.haskell.org/packages/archive/00-index.tar.gz

echo "Compiling depparse..."
ghc depparse.hs -outputdir /tmp

echo "Crawling dependency graph..."
./crawl.py

echo "Done."
