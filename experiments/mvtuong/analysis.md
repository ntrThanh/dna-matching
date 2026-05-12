# Algorithm comparison - mvtuong

This folder originally contained two approaches for DNA k-mismatch matching:

1. `RabinKarp`
2. `DPEditDistance`

## Comparison

`RabinKarp` is easier to maintain in this project:

- The idea is direct: rolling hash for fast filtering, then exact mismatch counting.
- The implementation matches the k-mismatch problem definition used by the dataset.
- Runtime is lightweight for exact matching and the control flow is easy to explain.

`DPEditDistance` was harder to justify and explain:

- It mixed two different ideas in one class: simple k-mismatch matching and full edit distance.
- The class name suggested Levenshtein distance, but `run()` actually used mismatch counting.
- It introduced a more expensive dynamic-programming interpretation without a clear need in this experiment.

## Decision

`DPEditDistance` was removed from this folder.

The maintained algorithm is `RabinKarp`, because it is the clearer fit for the current experiment and easier to explain to readers.
