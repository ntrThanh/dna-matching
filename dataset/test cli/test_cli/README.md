# CLI test files

Run examples from the project root:

```bash
python3 main.py -t "dataset/test cli/test_cli/dna_exact.txt" -p "dataset/test cli/test_cli/pattern_exact.txt" -k 0 -a brute_force
python3 main.py -t "dataset/test cli/test_cli/dna_approx.txt" -p "dataset/test cli/test_cli/pattern_approx.txt" -k 1 -a kmp
python3 main.py -t "dataset/test cli/test_cli/dna_fasta.txt" -p "dataset/test cli/test_cli/pattern_fasta.txt" -k 0 -a suffix_array
python3 main.py -t "dataset/test cli/test_cli/dna_long_2000.txt" -p "dataset/test cli/test_cli/pattern_long_k2.txt" -k 2 -a boyer_moore
```

The long test case has a DNA sequence of 2000 bases. With `k=2`, the expected match starts at index `900`.
