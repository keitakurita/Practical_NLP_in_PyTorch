#!/bin/bash

echo "- Downloading Penn Treebank (PTB)"
if [[ ! -d 'penn' ]]; then
    wget --quiet --continue http://www.fit.vutbr.cz/~imikolov/rnnlm/simple-examples.tgz
    tar -xzf simple-examples.tgz

    mkdir -p penn
    cd penn
    mv ../simple-examples/data/ptb.train.txt train.txt
    mv ../simple-examples/data/ptb.test.txt test.txt
    mv ../simple-examples/data/ptb.valid.txt valid.txt
    cd ..

    echo "- Downloading Penn Treebank (Character)"
    mkdir -p pennchar
    cd pennchar
    mv ../simple-examples/data/ptb.char.train.txt train.txt
    mv ../simple-examples/data/ptb.char.test.txt test.txt
    mv ../simple-examples/data/ptb.char.valid.txt valid.txt
    cd ..

    rm -rf simple-examples/
fi

