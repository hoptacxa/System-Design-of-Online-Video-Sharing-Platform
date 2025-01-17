#!/bin/bash
# Get your keybindings from ~/Library/Application Support/Code/User/keybindings.json
LAST_TEST_MATCHER=`cat ./last-test-matcher.txt`
./exec-test $LAST_TEST_MATCHER
