import argparse
import json
import time
from pathlib import Path

from experiments.mvtuong.rabin_karp import RabinKarp
from experiments.ndtam.kmp import KMPWithVerification
from experiments.ntthanh.boyer_moore import BoyerMooreWithVerification
from experiments.ntthanh.suffix_tree import SuffixTreeWithBacktracking
from experiments.nvtai.brute_force import BruteForceKMismatches
from experiments.nvtai.suffix_array import SuffixArrayWithCandidateVerification


ALGORITHMS = {
    "brute_force": BruteForceKMismatches,
    "bruteforce": BruteForceKMismatches,
    "bf": BruteForceKMismatches,
    "rabin_karp": RabinKarp,
    "rabinkarp": RabinKarp,
    "rk": RabinKarp,
    "kmp": KMPWithVerification,
    "boyer_moore": BoyerMooreWithVerification,
    "boyermoore": BoyerMooreWithVerification,
    "bm": BoyerMooreWithVerification,
    "suffix_array": SuffixArrayWithCandidateVerification,
    "suffixarray": SuffixArrayWithCandidateVerification,
    "sa": SuffixArrayWithCandidateVerification,
    "suffix_tree": SuffixTreeWithBacktracking,
    "suffixtree": SuffixTreeWithBacktracking,
    "st": SuffixTreeWithBacktracking,
}


def normalize_algorithm_name(name):
    return name.strip().lower().replace("-", "_").replace(" ", "_")


def get_algorithm(name):
    key = normalize_algorithm_name(name)
    if key not in ALGORITHMS:
        valid_names = ", ".join(sorted(ALGORITHMS))
        raise ValueError(f"Unknown algorithm '{name}'. Valid names: {valid_names}")
    return ALGORITHMS[key]()


def read_sequence(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    sequence_lines = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith(">"):
            continue
        sequence_lines.append(line)

    return "".join(sequence_lines).upper()


def run_algorithm(text, pattern, k=0, algorithm="brute_force", evaluate=True):
    algo = get_algorithm(algorithm)
    if evaluate:
        return algo.evaluate(text.upper(), pattern.upper(), k)

    return algo.run(text.upper(), pattern.upper(), k)


def run_algorithm_from_files(text_file, pattern_file, k=0, algorithm="brute_force"):
    total_start = time.perf_counter()

    read_start = time.perf_counter()
    text = read_sequence(text_file)
    pattern = read_sequence(pattern_file)
    read_end = time.perf_counter()

    result = run_algorithm(text, pattern, k=k, algorithm=algorithm, evaluate=True)
    total_end = time.perf_counter()

    result["file_read_runtime_sec"] = read_end - read_start
    result["total_runtime_sec"] = total_end - total_start
    return result


def build_parser():
    parser = argparse.ArgumentParser(
        description="Run DNA matching algorithms from code or CLI."
    )
    parser.add_argument(
        "-t",
        "--text-file",
        required=True,
        help="Path to text file containing the DNA sequence.",
    )
    parser.add_argument(
        "-p",
        "--pattern-file",
        required=True,
        help="Path to text file containing the DNA pattern.",
    )
    parser.add_argument(
        "-k",
        type=int,
        default=0,
        help="Maximum number of mismatches allowed. Default: 0.",
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        required=True,
        help=(
            "Algorithm name. Examples: brute_force, rabin_karp, kmp, "
            "boyer_moore, suffix_array, suffix_tree."
        ),
    )
    parser.add_argument(
        "--matches-only",
        action="store_true",
        help="Print only the list of matching positions.",
    )
    return parser


def main():
    args = build_parser().parse_args()
    result = run_algorithm_from_files(
        text_file=args.text_file,
        pattern_file=args.pattern_file,
        k=args.k,
        algorithm=args.algorithm,
    )

    output = result["matches"] if args.matches_only else result
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
