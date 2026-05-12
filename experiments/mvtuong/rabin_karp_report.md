# Báo cáo Phân tích Thuật toán: Rabin-Karp with Verification

## 1. Phân tích bài toán
Bài toán yêu cầu tìm kiếm vị trí xuất hiện của một chuỗi mẫu (pattern) có độ dài $M$ bên trong một chuỗi văn bản (text) có độ dài $N$, với giới hạn sai lệch tối đa là $k$ (mismatches).

Thuật toán **Rabin-Karp with Verification** giải quyết bài toán này bằng cách kết hợp:
- **Rolling Hash** để biểu diễn nhanh giá trị băm của `pattern` và từng cửa sổ độ dài $M$ trong `text`.
- **Verification** để kiểm tra lại trực tiếp từng vị trí nghi ngờ, nhằm đảm bảo kết quả đúng tuyệt đối.

Ý tưởng chính:
- Với mỗi ký tự DNA (`A`, `C`, `G`, `T`), thuật toán ánh xạ chúng sang số nguyên nhỏ.
- Sau đó tính hash của `pattern` và hash của từng cửa sổ `text[i:i+M]`.
- Khi cần dịch sang cửa sổ tiếp theo, thuật toán không tính lại từ đầu mà dùng **rolling hash** để cập nhật trong thời gian hằng số.
- Khi `k = 0`, thuật toán dùng **2 hàm hash độc lập** như một bộ lọc mạnh: chỉ khi cả hai hash trùng nhau mới xác minh trực tiếp.
- Khi `k > 0`, implementation hiện tại vẫn giữ rolling hash, nhưng **xác minh trực tiếp trên mọi cửa sổ** để không bỏ sót trường hợp có mismatch hợp lệ. Nói cách khác, hash lúc này chủ yếu còn vai trò hỗ trợ cho trường hợp exact match, còn tính đúng đắn được đảm bảo bởi bước verification.

Phương pháp này phù hợp với dữ liệu DNA vì:
- Bảng chữ cái nhỏ, cố định.
- Rolling hash cài đặt gọn.
- Verification có thể dừng sớm ngay khi số lỗi vượt quá $k$.

## 2. Xác định Input / Output
- **Input:**
  - `text` (chuỗi): Chuỗi DNA gốc (genome hoặc sequence dài) cần tìm kiếm.
  - `pattern` (chuỗi): Chuỗi DNA mẫu cần tìm.
  - `k` (số nguyên): Số lượng ký tự sai lệch tối đa (mismatches) cho phép.
- **Output:**
  - `list[int]`: Danh sách vị trí các chỉ số (index) bắt đầu trong chuỗi `text` mà `pattern` khớp với số sai lệch $\le k$.

## 3. Pseudocode (Mã giả)

```text
// Hàm phụ trợ: mã hóa ký tự DNA
Hàm ENCODE(ch):
    Nếu ch == 'A': trả về 1
    Nếu ch == 'C': trả về 2
    Nếu ch == 'G': trả về 3
    Nếu ch == 'T': trả về 4
    Ngược lại: trả về 0

// Hàm phụ trợ: xác minh số mismatch
Hàm COUNT_MISMATCH(text, start, pattern, k):
    mismatches = 0
    Với j từ 0 đến len(pattern) - 1:
        Nếu text[start + j] != pattern[j]:
            mismatches = mismatches + 1
            Nếu mismatches > k:
                Trả về False
    Trả về True

// Hàm chính: Rabin-Karp with Verification
Hàm RABIN_KARP_WITH_VERIFICATION(text, pattern, k):
    n = len(text), m = len(pattern)
    Nếu m > n:
        Trả về []

    Tính hash kép của pattern: ph1, ph2
    Tính hash kép của cửa sổ đầu tiên trong text: wh1, wh2
    Tính highest_power cho từng modulus

    results = []

    Với i từ 0 đến n - m:
        Nếu k == 0:
            Nếu wh1 == ph1 và wh2 == ph2:
                Nếu COUNT_MISMATCH(text, i, pattern, k) == True:
                    Thêm i vào results
        Ngược lại:
            Nếu COUNT_MISMATCH(text, i, pattern, k) == True:
                Thêm i vào results

        Nếu i < n - m:
            Cập nhật wh1, wh2 bằng rolling hash

    Trả về results
```

## 4. Đánh giá độ phức tạp
- **Giai đoạn tiền xử lý:**
  - Mã hóa và tính hash của `pattern`: $O(M)$.
  - Tính hash của cửa sổ đầu tiên trong `text`: $O(M)$.
  - Tổng tiền xử lý: $O(M)$.

- **Trường hợp tìm kiếm chính xác ($k = 0$):**
  - Mỗi cửa sổ được cập nhật hash trong $O(1)$.
  - Chỉ những cửa sổ có hash kép trùng mới cần xác minh.
  - **Thời gian trung bình:** gần $O(N + M)$.
  - **Thời gian tệ nhất:** $O(N \cdot M)$ nếu có nhiều va chạm hash hoặc nhiều lần phải verification.

- **Trường hợp tìm kiếm xấp xỉ ($k > 0$):**
  - Implementation hiện tại xác minh trực tiếp mọi cửa sổ độ dài $M$ trong `text`.
  - Có tổng cộng $N - M + 1$ cửa sổ, mỗi lần xác minh tốn tối đa $O(M)$.
  - **Thời gian tổng quát:** $O((N - M + 1) \cdot M)$, thường viết gọn là $O(N \cdot M)$.
  - Trong thực tế, bước verification có thể dừng sớm khi số mismatch vượt quá $k$, nên thời gian thực tế thường tốt hơn trường hợp xấu nhất.

- **Độ phức tạp không gian (Space Complexity):**
  - Chỉ dùng một số biến hash, hằng số, và danh sách kết quả.
  - **Không gian phụ trợ:** $O(1)$, chưa tính kích thước output.

## Nhận xét
- Điểm mạnh của thuật toán là cài đặt gọn, dễ kiểm chứng, ít tốn bộ nhớ.
- Với bài toán exact match (`k = 0`), rolling hash giúp lọc rất hiệu quả.
- Với bài toán approximate match (`k > 0`), implementation hiện tại ưu tiên tính đúng đắn hơn là tối ưu hóa tốc độ, vì vẫn phải xác minh trực tiếp trên từng cửa sổ.
