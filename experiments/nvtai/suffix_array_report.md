# Báo cáo Phân tích Thuật toán: Suffix Array with Candidate Verification

## 1. Phân tích bài toán
Bài toán cần tìm các vị trí trong `text` sao cho `pattern` khớp với chuỗi con tương ứng và có tối đa `k` mismatch.

Suffix Array lưu danh sách các vị trí bắt đầu của mọi suffix trong `text`, được sắp xếp theo thứ tự từ điển. Với khớp chính xác, ta có thể tìm `pattern` bằng binary search trên suffix array.

Với khớp xấp xỉ, thuật toán sử dụng nguyên lý chia `pattern` thành `k + 1` đoạn:
- Nếu toàn bộ `pattern` khớp với tối đa `k` mismatch, thì ít nhất một trong `k + 1` đoạn phải khớp chính xác.
- Dùng suffix array để tìm các vị trí khớp chính xác của từng đoạn.
- Từ vị trí khớp của đoạn, suy ra candidate start của pattern đầy đủ.
- Verify lại từng candidate bằng cách đếm mismatch trên toàn pattern.

## 2. Input / Output
- **Input**
  - `text`: chuỗi DNA gốc.
  - `pattern`: chuỗi DNA cần tìm.
  - `k`: số mismatch tối đa cho phép.
- **Output**
  - `list[int]`: danh sách vị trí bắt đầu trong `text` có mismatch `<= k`.

## 3. Pseudocode

```text
Hàm BUILD_SUFFIX_ARRAY(text):
    Trả về tất cả chỉ số i của text, được sắp xếp theo text[i:]

Hàm FIND_EXACT_SEGMENT(text, suffix_array, segment):
    Dùng binary search để tìm khoảng suffix có tiền tố bằng segment
    Trả về các vị trí suffix trong khoảng đó

Hàm SUFFIX_ARRAY_CANDIDATE_VERIFICATION(text, pattern, k):
    Nếu pattern rỗng hoặc len(pattern) > len(text):
        Trả về []

    Nếu k >= len(pattern):
        Trả về mọi vị trí bắt đầu hợp lệ trong text

    suffix_array = BUILD_SUFFIX_ARRAY(text)

    Nếu k == 0:
        Trả về FIND_EXACT_SEGMENT(text, suffix_array, pattern)

    Chia pattern thành k + 1 đoạn gần bằng nhau
    candidates = tập rỗng

    Với mỗi segment tại offset trong pattern:
        segment_matches = FIND_EXACT_SEGMENT(text, suffix_array, segment)
        Với mỗi match_pos trong segment_matches:
            candidate_start = match_pos - offset
            Nếu candidate_start hợp lệ:
                Thêm candidate_start vào candidates

    results = []
    Với mỗi candidate trong candidates:
        Đếm mismatch giữa pattern và text[candidate:candidate + len(pattern)]
        Nếu mismatch <= k:
            Thêm candidate vào results

    Trả về results đã sắp xếp
```

## 4. Độ phức tạp
Gọi `N = len(text)`, `M = len(pattern)`.

- **Build suffix array**
  - Cài đặt Python hiện tại sắp xếp suffix bằng `text[i:]`, nên chi phí thực tế có thể tới `O(N^2 log N)` do tạo và so sánh suffix.
  - Nếu dùng thuật toán suffix array tối ưu, có thể giảm xuống `O(N log N)` hoặc `O(N)`.

- **Tìm exact segment**
  - Binary search trên suffix array cần `O(log N)` phép so sánh.
  - Mỗi phép so sánh nhìn tối đa độ dài segment.
  - Việc lấy các match tốn `O(occ_segment)`.

- **Verification**
  - Nếu có `C` candidate, chi phí verify là `O(C * M)`.

- **Tổng thể**
  - Phụ thuộc số candidate sinh ra. Khi `k` nhỏ và segment đủ dài, filter bằng suffix array giúp giảm số candidate cần verify.

## 5. Nhận xét
Suffix Array tiết kiệm bộ nhớ hơn Suffix Tree và phù hợp cho truy vấn lặp lại trên cùng một text. Trong implementation này, suffix array được build mỗi lần `run`, nên phù hợp với benchmark đơn lẻ; nếu cần chạy nhiều pattern trên cùng genome, nên cache suffix array theo `text`.
