# Báo cáo Phân tích Thuật toán: Brute Force with k mismatches

## 1. Phân tích bài toán
Bài toán DNA Matching yêu cầu tìm tất cả vị trí bắt đầu trong chuỗi `text` sao cho chuỗi con có cùng độ dài với `pattern` khác `pattern` không quá `k` ký tự.

Thuật toán Brute Force kiểm tra trực tiếp mọi vị trí có thể trong `text`. Tại mỗi vị trí, thuật toán so sánh từng ký tự của `pattern` với chuỗi con tương ứng trong `text`, đếm số mismatch và dừng sớm khi số mismatch vượt quá `k`.

Đây là baseline quan trọng vì cách cài đặt đơn giản, dễ kiểm chứng và phù hợp để đối chiếu độ chính xác của các thuật toán tối ưu hơn.

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
- **Thời gian**
  - Trường hợp xấu nhất: `O((N - M + 1) * M)`, tương đương `O(NM)`.
  - Trong thực tế có dừng sớm khi mismatch vượt quá `k`, nên với `k` nhỏ có thể nhanh hơn.
- **Không gian**
  - `O(1)` ngoài danh sách kết quả.
  - Nếu tính cả output thì `O(occ)`, với `occ` là số vị trí match.

## 5. Nhận xét
Brute Force không phù hợp với genome rất lớn nếu pattern dài, nhưng rất phù hợp làm mốc đối chiếu độ chính xác cho các thuật toán khác.
