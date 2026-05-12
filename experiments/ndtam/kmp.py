import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from base_class import Algorithm


class KMPWithVerification(Algorithm):
    def __init__(self, name="KMP-based Filtering + Verification"):
        super().__init__(name)

    def _build_failure(self, pattern: str) -> list:
        m = len(pattern)
        failure = [0] * m
        j = 0  

        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = failure[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            failure[i] = j

        return failure

    def _kmp_search(self, text: str, pattern: str) -> list:
        n = len(text)
        m = len(pattern)

        if m == 0:
            return []
        if m > n:
            return []

        failure = self._build_failure(pattern)
        results = []
        j = 0  
        for i in range(n):
            while j > 0 and text[i] != pattern[j]:
                j = failure[j - 1]
            if text[i] == pattern[j]:
                j += 1
            if j == m:
                results.append(i - m + 1)
                j = failure[j - 1]

        return results

    def _count_mismatches(self, text: str, start: int, pattern: str, k: int) -> int:
        mismatches = 0
        m = len(pattern)
        for j in range(m):
            if text[start + j] != pattern[j]:
                mismatches += 1
                if mismatches > k:
                    return mismatches
        return mismatches

    def run(self, text: str, pattern: str, k: int = 0) -> list:
        n = len(text)
        m = len(pattern)

        if m == 0:
            return []
        if n < m:
            return []
        if k >= m:
            return list(range(n - m + 1))

        if k == 0:
            return self._kmp_search(text, pattern)

        num_segments = k + 1
        segment_len = m // num_segments  

        candidates = set()

        for i in range(num_segments):
            seg_start = i * segment_len
            seg_end = m if i == num_segments - 1 else (i + 1) * segment_len
            segment = pattern[seg_start:seg_end]

            if len(segment) == 0:
                continue

            seg_matches = self._kmp_search(text, segment)

            for match_pos in seg_matches:
                candidate_start = match_pos - seg_start
                if 0 <= candidate_start <= n - m:
                    candidates.add(candidate_start)

        results = []
        for cand in sorted(candidates):
            mismatches = self._count_mismatches(text, cand, pattern, k)
            if mismatches <= k:
                results.append(cand)

        return results


if __name__ == '__main__':
    algo = KMPWithVerification()
    print("Exact Match (k=0):        ", algo.evaluate("GATACGA", "GA", 0))
    print("Approximate Match (k=1):  ", algo.evaluate("GATACGA", "GA", 1))
    print("DNA test (k=0):           ", algo.evaluate("ACGTACGTACGT", "ACGT", 0))
    print("DNA test (k=1):           ", algo.evaluate("ACGAACGT", "ACGT", 1))
    print("KMP failure table test:   ", algo.evaluate("AABAACAADAABAAABAA", "AABAA", 0))
