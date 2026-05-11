import bisect
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from base_class import Algorithm


class SuffixArrayWithCandidateVerification(Algorithm):
    def __init__(self, name="Suffix Array with Candidate Verification"):
        super().__init__(name)

    def build_suffix_array(self, text):
        return sorted(range(len(text)), key=lambda i: text[i:])

    def suffix_key(self, text, suffix_start, length):
        return text[suffix_start:suffix_start + length]

    def find_exact_segment(self, text, suffix_array, segment):
        if not segment:
            return []

        seg_len = len(segment)
        keys = [self.suffix_key(text, i, seg_len) for i in suffix_array]

        left = bisect.bisect_left(keys, segment)
        right = bisect.bisect_right(keys, segment)

        return suffix_array[left:right]

    def verify_candidate(self, text, pattern, start, k):
        mismatches = 0
        for j, p_char in enumerate(pattern):
            if text[start + j] != p_char:
                mismatches += 1
                if mismatches > k:
                    return False
        return True

    def run(self, text, pattern, k=0):
        n = len(text)
        m = len(pattern)

        if m == 0 or m > n:
            return []

        if k >= m:
            return list(range(n - m + 1))

        suffix_array = self.build_suffix_array(text)

        if k == 0:
            matches = self.find_exact_segment(text, suffix_array, pattern)
            return sorted(pos for pos in matches if pos <= n - m)

        num_segments = k + 1
        base_len = m // num_segments
        remainder = m % num_segments

        candidates = set()
        offset = 0

        for segment_id in range(num_segments):
            segment_len = base_len + (1 if segment_id < remainder else 0)
            segment = pattern[offset:offset + segment_len]

            for match_pos in self.find_exact_segment(text, suffix_array, segment):
                candidate_start = match_pos - offset
                if 0 <= candidate_start <= n - m:
                    candidates.add(candidate_start)

            offset += segment_len

        return [
            start
            for start in sorted(candidates)
            if self.verify_candidate(text, pattern, start, k)
        ]


if __name__ == "__main__":
    algo = SuffixArrayWithCandidateVerification()
    print("Exact Match (k=0):", algo.evaluate("GATACGA", "GA", 0))
    print("Approximate Match (k=1):", algo.evaluate("GATACGA", "GA", 1))
