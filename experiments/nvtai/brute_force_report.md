# Báo cáo Phân tích Thuật toán: Brute Force with k mismatches

## 1. Phân tích bài toán
Bài toán DNA Matching cần tìm tất cả vị trí trong chuỗi `text` mà tại đó `pattern` xuất hiện với số ký tự sai khác không vượt quá `k`. Với mỗi vị trí `i`, ta so sánh `pattern` với đoạn `text[i:i + len(pattern)]`; nếu số mismatch `<= k` thì `i` được đưa vào kết quả.

Vấn đề chính là phải kiểm tra nhiều vị trí ứng viên trong `text`, trong khi vẫn cho phép một số sai lệch nhất định do đột biến hoặc lỗi dữ liệu. Khi `k = 0`, đây là bài toán khớp chính xác; khi `k > 0`, đây là khớp xấp xỉ theo số mismatch.

Ý tưởng của Brute Force là duyệt lần lượt mọi vị trí bắt đầu có thể, so sánh từng ký tự của `pattern` với chuỗi con tương ứng trong `text`, rồi đếm mismatch. Nếu số mismatch vượt quá `k`, thuật toán dừng sớm tại vị trí hiện tại và chuyển sang vị trí tiếp theo.

Thuật toán này đơn giản, không cần tiền xử lý và rất phù hợp làm baseline để kiểm tra tính đúng của các thuật toán khác. Đổi lại, nó không hiệu quả trên genome lớn vì phải thử gần như toàn bộ vị trí trong `text`.

## 2. Input / Output
- **Input**
  - `text`: chuỗi DNA gốc.
  - `pattern`: chuỗi DNA cần tìm.
  - `k`: số mismatch tối đa cho phép.
- **Output**
  - `list[int]`: danh sách vị trí bắt đầu trong `text` có mismatch `<= k`.

## 3. Pseudocode

```text
Hàm BRUTE_FORCE_K_MISMATCHES(text, pattern, k):
    n = len(text)
    m = len(pattern)

    Nếu m == 0 hoặc m > n:
        Trả về []

    results = []

    Với i từ 0 đến n - m:
        mismatches = 0

        Với j từ 0 đến m - 1:
            Nếu text[i + j] != pattern[j]:
                mismatches += 1
                Nếu mismatches > k:
                    Thoát vòng lặp

        Nếu mismatches <= k:
            Thêm i vào results

    Trả về results
```

## 4. Độ phức tạp
Gọi `N = len(text)` và `M = len(pattern)`. Thuật toán cần kiểm tra `N - M + 1` vị trí bắt đầu trong `text`.

- **Thời gian tiền xử lý:** `O(1)` vì không cần xây dựng cấu trúc dữ liệu phụ.

- **Thời gian xấu nhất:** `O((N - M + 1) * M)`, thường viết gọn là `O(NM)`. Trường hợp này xảy ra khi mỗi vị trí phải so sánh gần như toàn bộ pattern trước khi kết luận.

- **Thời gian tốt hơn trong thực tế:** nếu mismatch vượt quá `k` sớm, thuật toán dừng ngay tại vị trí đó. Vì vậy với `k` nhỏ, thời gian thực tế có thể thấp hơn đáng kể so với worst-case.

- **Không gian:** `O(1)` nếu không tính output, vì chỉ dùng các biến đếm. Nếu có `occ` vị trí match, bộ nhớ cho danh sách kết quả là `O(occ)`.

## 5. Nhận xét
Brute Force không phù hợp với genome rất lớn nếu pattern dài, nhưng rất phù hợp làm mốc đối chiếu độ chính xác cho các thuật toán khác.
