# Báo cáo Phân tích Thuật toán: KMP-based Filtering + Verification

## 1. Phân tích bài toán

Bài toán yêu cầu tìm tất cả vị trí xuất hiện của chuỗi mẫu (pattern) có độ dài $M$ trong chuỗi văn bản (text) có độ dài $N$, với tối đa $k$ ký tự sai lệch (**Hamming distance** — chỉ substitution).

Trong bối cảnh DNA Matching:
- **Text ($T$)**: Chuỗi hệ gen (genome) hoặc đoạn DNA dài (vd: E. coli genome).
- **Pattern ($P$)**: Đoạn DNA ngắn cần tìm kiếm (ví dụ: gen, exon, đoạn mồi).
- **k**: Số lượng đột biến điểm (point mutation) cho phép.

Thuật toán **KMP-based Filtering + Verification** hoạt động theo hai giai đoạn, dựa trên **Nguyên lý Chuồng Bồ Câu (Pigeonhole Principle)**:

> Nếu pattern khớp với một đoạn text với tối đa $k$ mismatch, thì khi chia pattern thành $k+1$ đoạn (segments), **ít nhất 1 đoạn phải khớp chính xác 100%** với text tại đó.

- **Giai đoạn Lọc (Filtering)**: Dùng KMP tìm chính xác từng đoạn nhỏ → sinh ra tập ứng viên (candidates).
- **Giai đoạn Xác minh (Verification)**: Đếm mismatch toàn pattern tại mỗi candidate, chỉ giữ lại vị trí có ≤ $k$ sai lệch.

KMP được chọn làm bộ lọc chính nhờ độ phức tạp tuyến tính $O(N + M/k)$ và tính ổn định (không có trường hợp xấu như Boyer-Moore trên DNA alphabet nhỏ).

---

## 2. Xác định Input / Output

- **Input:**
  - `text` (chuỗi): Chuỗi DNA gốc cần tìm kiếm.
  - `pattern` (chuỗi): Chuỗi DNA mẫu cần khớp trong `text`.
  - `k` (số nguyên ≥ 0): Số lượng ký tự sai lệch tối đa cho phép.

- **Output:**
  - `list[int]`: Danh sách các chỉ số bắt đầu (0-indexed) trong `text` tại đó `pattern` khớp với số sai lệch ≤ $k$, được sắp xếp tăng dần.

---

## 3. Pseudocode (Mã giả)

```text
//HÀM PHỤ TRỢ 1: Xây dựng bảng Failure Function (KMP)
Hàm BUILD_FAILURE(pattern):
    m = len(pattern)
    failure[0..m-1] = [0] * m
    j = 0   // độ dài prefix đang xét
    Với i từ 1 đến m-1:
        Trong khi j > 0 và pattern[i] != pattern[j]:
            j = failure[j-1]
        Nếu pattern[i] == pattern[j]:
            j = j + 1
        failure[i] = j
    Trả về failure

// HÀM PHỤ TRỢ 2: KMP tìm chính xác 
Hàm KMP_SEARCH(text, pattern):
    failure = BUILD_FAILURE(pattern)
    j = 0   // số ký tự đã khớp
    results = []
    Với i từ 0 đến n-1:
        Trong khi j > 0 và text[i] != pattern[j]:
            j = failure[j-1]
        Nếu text[i] == pattern[j]:
            j = j + 1
        Nếu j == len(pattern):
            Thêm (i - len(pattern) + 1) vào results
            j = failure[j-1]
    Trả về results

//HÀM CHÍNH: KMP Filtering + Verification
Hàm KMP_WITH_VERIFICATION(text, pattern, k):
    Nếu k == 0:
        Trả về KMP_SEARCH(text, pattern)

    num_segments = k + 1
    segment_len  = len(pattern) // num_segments
    candidates   = Tập rỗng

    // GIAI ĐOẠN 1: FILTERING 
    Với i từ 0 đến num_segments - 1:
        seg_start = i * segment_len
        seg_end   = len(pattern) nếu i == num_segments - 1
                    ngược lại (i+1) * segment_len
        segment   = pattern[seg_start:seg_end]

        seg_matches = KMP_SEARCH(text, segment)

        Với mỗi match_pos trong seg_matches:
            candidate_start = match_pos - seg_start
            Nếu 0 <= candidate_start <= n - m:
                Thêm candidate_start vào candidates

    // GIAI ĐOẠN 2: VERIFICATION
    final_results = []
    Với mỗi cand trong sorted(candidates):
        mismatches = 0
        Với j từ 0 đến m-1:
            Nếu text[cand + j] != pattern[j]:
                mismatches = mismatches + 1
            Nếu mismatches > k:
                Thoát vòng lặp   // early termination
        Nếu mismatches <= k:
            Thêm cand vào final_results

    Trả về final_results
```

---

## 4. Đánh giá độ phức tạp

### Thời gian (Time Complexity)

**Giai đoạn Filtering:**
- Mỗi segment có độ dài $\approx M/(k+1)$.
- KMP tìm 1 segment trong text: $O(N + M/(k+1))$.
- Chạy $k+1$ lần (cho tất cả segments):

$$O\left((k+1) \cdot \left(N + \frac{M}{k+1}\right)\right) = O(k \cdot N + M)$$

**Giai đoạn Verification:**
- Gọi $C$ là số lượng candidates. Mỗi verification tốn $O(M)$ với early termination.
- Trong thực tế, $C$ nhỏ khi $M/(k+1)$ đủ lớn (ít false positives).

$$O(C \cdot M)$$

**Tổng độ phức tạp thời gian:**

$$O(k \cdot N + M + C \cdot M)$$

| Trường hợp | Độ phức tạp |
|---|---|
| Build failure table (mỗi segment) | $O(M/(k+1))$ |
| Filtering ($k+1$ lần KMP) | $O(k \cdot N + M)$ |
| Verification ($C$ candidates) | $O(C \cdot M)$ |
| **Tổng** | $O(k \cdot N + C \cdot M)$ |

### Không gian (Space Complexity)

$$O(M + C)$$

- $O(M/(k+1))$ cho failure table mỗi đoạn → $O(M)$.
- $O(C)$ để lưu tập candidates.
- Rất tiết kiệm bộ nhớ so với Suffix Tree ($O(N)$ node) hay DP ($O(N \cdot M)$).

### Nhận xét chất lượng bộ lọc

- **Lọc tốt khi $M/(k+1)$ lớn**: Các đoạn dài khó khớp ngẫu nhiên trên DNA (alphabet 4 ký tự) → ít false positives $C \approx$ occ.
- **Lọc kém khi $k/M$ lớn** (tỷ lệ lỗi cao): Các đoạn rất ngắn → nhiều false positives → giai đoạn verification chiếm ưu thế.
- **Ổn định (Stable)**: KMP không có trường hợp xấu — luôn $O(N)$ mỗi lần tìm, phù hợp với DNA có alphabet nhỏ $|\Sigma|=4$ (Boyer-Moore có thể bị giảm hiệu quả).

### So sánh với các thuật toán khác

| Thuật toán | Thời gian | Không gian | Ghi chú |
|---|---|---|---|
| Brute Force | $O(N \cdot M)$ | $O(1)$ | Chậm, không filter |
| **KMP + Verification** | $O(k \cdot N + C \cdot M)$ | $O(M)$ | **Ổn định, tuyến tính** |
| Boyer-Moore + Verif. | $O(k \cdot N/m + C \cdot M)$ | $O(M)$ | Nhanh hơn khi $M$ lớn |
| Bitap / Shift-Or | $O(N \cdot k)$ | $O(M + k)$ | Không inner loop |
| DP Edit Distance | $O(N \cdot M)$ | $O(M)$ | Hỗ trợ insert/delete |
