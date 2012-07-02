#!/bin/sh
echo "Downloading index..."
curl -O http://hackage.haskell.org/packages/archive/00-index.tar.gz

echo "Extracting index..."
mkdir index
tar -C index -xzf 00-index.tar.gz

echo "Compiling depparse..."
ghc depparse.hs -outputdir /tmp

echo "Crawling dependency graph..."
./crawl.py

echo "Done."
