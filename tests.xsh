#!/usr/bin/env xonsh
import os
$RAISE_SUBPROC_ERROR = True
os.environ['modelci_root'] = $(pwd).strip()
$modelci_root = $(pwd).strip()

./utils_test.xsh
./core_test.xsh
./repo_test.xsh
./baseline_strategy_test.xsh
./core_test.xsh
