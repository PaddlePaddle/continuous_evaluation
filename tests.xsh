#!/usr/bin/env xonsh
$RAISE_SUBPROC_ERROR = True

./utils_test.xsh
./core_test.xsh
./repo_test.xsh
./baseline_strategy_test.xsh
./core_test.xsh