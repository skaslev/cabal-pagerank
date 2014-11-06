#!/bin/sh
echo "Downloading index..."
wget http://hackage.haskell.org/packages/index.tar.gz

echo "Extracting index..."
mkdir index
tar -C index -xf index.tar.gz

echo "Compiling depparse..."
ghc depparse.hs -outputdir /tmp

echo "Crawling dependency graph..."
./crawl.py

echo "Done."
