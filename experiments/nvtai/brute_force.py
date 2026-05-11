import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from base_class import Algorithm


class BruteForceKMismatches(Algorithm):
    def __init__(self, name="Brute Force with k mismatches"):
        super().__init__(name)

    def run(self, text, pattern, k=0):
        n = len(text)
        m = len(pattern)

        if m == 0 or m > n:
            return []

        results = []
        for i in range(n - m + 1):
            mismatches = 0
            for j in range(m):
                if text[i + j] != pattern[j]:
                    mismatches += 1
                    if mismatches > k:
                        break

            if mismatches <= k:
                results.append(i)

        return results


if __name__ == "__main__":
    algo = BruteForceKMismatches()
    print("Exact Match (k=0):", algo.evaluate("GATACGA", "GA", 0))
    print("Approximate Match (k=1):", algo.evaluate("GATACGA", "GA", 1))
