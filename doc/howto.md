# How-Tos

## Concepts

- `baseline`, one of the best KPI records in the history, the baseline should keep being updated.
- `Factor`, an alias for KPI to make the code more readable, developer can add more Factors to extend the MocroCE's tracked KPIs.

## Philosophy

`MacroCE` is a highly customizable framework which

- triggers the execution of every evaluation and compare the KPIs with baseline,
- helps to maintain the latest baseline,
- displays the evaluation status or human-readable reports with a web page, and give an alert by sending emails if the evaluation of some version fails.

It doesn't

- care about the details about the evaluation, in other words, one can embed any logics into an evaluation.


## Adding new KPIs

1. Reference [core.py](https://github.com/PaddlePaddle/MacroCE/blob/master/core.py), which defines the KPI base class called `Factor`.
2. Inherit `Factor` and implement all the `UnImplemented` methods, read the class `GreaterWorseFactor`.
3. Start a PR and merge the new KPI.

## Adding new evaluations

The baseline repo is at [baseline repo](https://github.com/Superjomn/paddle-modelci-baseline).

Let's take the existing evaluation [resnet30](https://github.com/Superjomn/paddle-modelci-baseline/tree/master/resnet30)
for example, the files required by `MacroCE` are

- `train.xsh`, it defines how to run this evaluation and generate the KPI records,
- `continuous_evaluation.py`, it tells `MacroCE` the KPI Factors this evaluation uses.
- `history/`, this is a directory and includes the baseline records.

The `train.xsh` is just a script and nothing to do with MacroCE so that one can embed any logics in it,
for example, any logics including data preparation, or even request a remote service.

The `continuous_evaluation.py` of `resnet30` looks like this.

```python
import os
import sys
sys.path.append(os.environ['modelci_root'])
from core import CostFactor, DurationFactor

train_cost_factor = CostFactor('train_cost', 0.15)
train_duration_factor = DurationFactor('train_duration', 0.15)

tracking_factors = [
    train_cost_factor,
    train_duration_factor,
]
```

it creates two instances of KPI Factors `train_cost_factor` and `train_duration_factor`,
both are defined in `MacroCE/core.py`.
The list `tracking_factors` is required by `MacroCE` which tells the KPIs this evaluation want to evaluate.

Into the details of `train.xsh`, the `resnet30/model.py` defines some details of running the model (MacroCE
do not care those logics, but the `train.xsh` need to add records to the KPI Factors in some way).

Some code snippets related to adding KPI records are as follows.

```python
# import KPI Factor instances
from continuous_evaluation import (train_cost_factor,
                                   train_duration_factor,
                                   tracking_factors)
# ...

for batch_id, data in enumerate(train_reader()):
    # ... train the model

    # add factor record
    train_cost_factor.add_record(np.array(avg_cost_, dtype='float32'))
    train_duration_factor.add_record(batch_end - batch_start)


# when the execution ends, persist all the factors to files.
for factor in tracking_factors:
    factor.persist()
```

## Running an evaluation locally

Each evaluation can execute seperately.

Lets take `resnet30` for example

```sh
git clone https://github.com/PaddlePaddle/MacroCE.git

cd MacroCE
git clone https://github.com/Superjomn/paddle-modelci-baseline.git models

cd models/resnet30
export modelci_root=`pwd`/../..
./train.xsh
```
