#!/usr/bin/env bash

# local -> remote
rsync -azP Analysis/ enricor@lisa.surfsara.nl:~/StackexchangeDatadumpQualityAnnotator/Analysis/

# remote -> local
rsync -azP enricor@lisa.surfsara.nl:~/StackexchangeDatadumpQualityAnnotator/Analysis/Data/ Analysis/Data
