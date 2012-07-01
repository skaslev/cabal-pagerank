#!/usr/bin/env runhaskell
import System.IO
import Data.Maybe
import Data.List
import Distribution.Package
import Distribution.PackageDescription
import Distribution.PackageDescription.Parse

getAllDeps gpd =
    nub $ map depName $ concat [
        buildDepends $ packageDescription gpd
      , maybe [] condTreeConstraints $ condLibrary gpd
      , concatMap (condTreeConstraints . snd) $ condExecutables gpd
    ]
  where depName (Dependency (PackageName name) _) = name

main = do
    content <- hGetContents stdin
    case parsePackageDescription content of
        --(ParseFailed error) -> putStrLn $ show error
        (ParseOk warnings pd) -> putStrLn $ show $ getAllDeps $ pd
