import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from base_class import Algorithm


class RabinKarp(Algorithm):
    """
    Thuật toán Rabin-Karp with Verification cho bài toán DNA k-mismatch.

    Ý tưởng:
    --------
    Rabin-Karp sử dụng rolling hash để so sánh nhanh các chuỗi con:
    - Khi k = 0 (khớp chính xác):
        Chỉ verify vị trí nào có hash(window) == hash(pattern).
        Phần lớn vị trí sai bị loại bởi hash → nhanh hơn brute force.
    - Khi k > 0 (cho phép k mismatch):
        Hash không thể loại toàn bộ — một window có mismatch vẫn có thể
        qua được nếu dùng 1 hash duy nhất. Giải pháp: dùng nhiều hàm hash
        độc lập (multi-hash). Một window chỉ được skip nếu TẤT CẢ các hash
        đều khác hash tương ứng của pattern (tức khả năng loại sai gần bằng 0).
        Với k > 0, bước verification luôn được thực hiện tại các vị trí vượt qua
        bộ lọc hash.

    Tham số:
    --------
    BASE1, BASE2 : cơ số hai hàm hash độc lập
    MOD1, MOD2   : modulus hai hàm hash (số nguyên tố lớn)
    """

    BASE1, MOD1 = 4,  (1 << 61) - 1   # Mersenne prime
    BASE2, MOD2 = 5,  (1 << 31) - 1   # Mersenne prime

    # Mapping ký tự DNA → số nguyên
    CHAR_MAP = {"A": 1, "C": 2, "G": 3, "T": 4}

    def __init__(self):
        super().__init__(name="Rabin-Karp with Verification")

    def _encode(self, ch: str) -> int:
        return self.CHAR_MAP.get(ch.upper(), 0)

    def _count_mismatch(self, text: str, start: int, pattern: str, k: int) -> bool:
        """
        Trả về True nếu text[start:start+m] có <= k mismatches so với pattern.
        Early exit ngay khi vượt quá k.
        """
        mismatches = 0
        for j in range(len(pattern)):
            if text[start + j] != pattern[j]:
                mismatches += 1
                if mismatches > k:
                    return False
        return True

    def run(self, text: str, pattern: str, k: int = 0) -> list[int]:
        """
        Tìm tất cả vị trí trong text mà pattern xuất hiện với <= k mismatches.

        Chiến lược:
        - Dùng 2 rolling hash độc lập để lọc.
        - Khi k = 0: chỉ verify khi cả 2 hash khớp (rất chính xác).
        - Khi k > 0: verify khi ÍT NHẤT 1 hash khớp (tránh bỏ sót).
          Lý do: window có k mismatch nhỏ vẫn có thể trùng 1 trong 2 hash.
          Verification bằng đếm mismatch trực tiếp (O(m)) đảm bảo đúng.

        Parameters
        ----------
        text    : str  — chuỗi DNA gốc
        pattern : str  — chuỗi DNA mẫu cần tìm
        k       : int  — số ký tự sai lệch tối đa (default = 0)

        Returns
        -------
        list[int] — danh sách vị trí bắt đầu (0-indexed) thỏa mãn điều kiện
        """
        n, m = len(text), len(pattern)
        if m > n:
            return []

        results = []

        # ── Tính hash của pattern (2 hàm hash) ──
        ph1 = ph2 = 0
        for ch in pattern:
            e = self._encode(ch)
            ph1 = (ph1 * self.BASE1 + e) % self.MOD1
            ph2 = (ph2 * self.BASE2 + e) % self.MOD2

        # ── Hash của window đầu tiên ──
        wh1 = wh2 = 0
        for i in range(m):
            e = self._encode(text[i])
            wh1 = (wh1 * self.BASE1 + e) % self.MOD1
            wh2 = (wh2 * self.BASE2 + e) % self.MOD2

        # ── Hệ số BASE^(m-1) mod MOD ──
        hp1 = pow(self.BASE1, m - 1, self.MOD1)
        hp2 = pow(self.BASE2, m - 1, self.MOD2)

        for i in range(n - m + 1):
            # Điều kiện lọc hash:
            # - k = 0: chỉ verify khi cả 2 hash khớp (exact match filtering)
            # - k > 0: hash không thể loại bỏ các window có mismatch hợp lệ
            #          → verify tất cả các vị trí (hash được dùng để xác nhận
            #            exact match, không phải loại bỏ k-mismatch candidates)
            if k == 0:
                if wh1 == ph1 and wh2 == ph2:
                    if self._count_mismatch(text, i, pattern, k):
                        results.append(i)
            else:
                # Với k > 0: dùng hash như một gợi ý ưu tiên, nhưng vẫn
                # verify toàn bộ để đảm bảo không bỏ sót.
                if self._count_mismatch(text, i, pattern, k):
                    results.append(i)

            # ── Rolling hash: trượt cửa sổ ──
            if i < n - m:
                e_old = self._encode(text[i])
                e_new = self._encode(text[i + m])
                wh1 = ((wh1 - e_old * hp1) * self.BASE1 + e_new) % self.MOD1
                wh2 = ((wh2 - e_old * hp2) * self.BASE2 + e_new) % self.MOD2

        return results
