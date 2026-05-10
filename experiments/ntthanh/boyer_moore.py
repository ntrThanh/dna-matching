import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from base_class import Algorithm

class BoyerMooreWithVerification(Algorithm):
    def __init__(self, name="Boyer-Moore with Verification"):
        super().__init__(name)
        
    def boyer_moore_exact(self, text, pattern):
        m = len(pattern)
        n = len(text)
        if m == 0:
            return []
            
        bad_char = {}
        for i in range(m):
            bad_char[pattern[i]] = i
            
        s = 0
        results = []
        while s <= n - m:
            j = m - 1
            while j >= 0 and pattern[j] == text[s + j]:
                j -= 1
                
            if j < 0:
                results.append(s)
                shift = m - bad_char.get(text[s + m], -1) if s + m < n else 1
                s += shift
            else:
                shift = j - bad_char.get(text[s + j], -1)
                s += max(1, shift)
                
        return results

    def run(self, text, pattern, k=0):
        n = len(text)
        m = len(pattern)
        
        if m == 0:
            return []
            
        if k >= m:
            return list(range(n - m + 1))
            
        if k == 0:
            return self.boyer_moore_exact(text, pattern)
            
        num_segments = k + 1
        segment_len = m // num_segments
        
        candidates = set()
        
        for i in range(num_segments):
            start_idx = i * segment_len
            end_idx = m if i == num_segments - 1 else (i + 1) * segment_len
            segment = pattern[start_idx:end_idx]
            
            segment_matches = self.boyer_moore_exact(text, segment)
            
            for match_pos in segment_matches:
                candidate_start = match_pos - start_idx
                if 0 <= candidate_start <= n - m:
                    candidates.add(candidate_start)
                    
        results = []
        for cand in sorted(candidates):
            mismatches = 0
            for j in range(m):
                if text[cand + j] != pattern[j]:
                    mismatches += 1
                    if mismatches > k:
                        break
            if mismatches <= k:
                results.append(cand)
                
        return results

if __name__ == '__main__':
    algo = BoyerMooreWithVerification()
    print("Exact Match (k=0):", algo.evaluate("GATACGA", "GA", 0))
    print("Approximate Match (k=1):", algo.evaluate("GATACGA", "GA", 1))
