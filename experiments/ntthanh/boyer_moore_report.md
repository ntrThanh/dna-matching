# Báo cáo Phân tích Thuật toán: Boyer-Moore with Verification

## 1. Phân tích bài toán
Bài toán yêu cầu tìm kiếm vị trí xuất hiện của một chuỗi mẫu (pattern) có độ dài $M$ bên trong một chuỗi văn bản (text) có độ dài $N$, với giới hạn sai lệch tối đa là $k$ (mismatches).

Thuật toán **Boyer-Moore with Verification** (Boyer-Moore kết hợp xác minh) giải quyết bài toán này dựa trên việc sử dụng **Nguyên lý Chuồng Bồ Câu (Pigeonhole Principle)**:
- Nếu chuỗi mẫu (pattern) khớp với văn bản với tối đa $k$ lỗi, thì khi ta chia mẫu đó thành $k + 1$ đoạn (segments), theo nguyên lý chuồng bồ câu, chắc chắn **phải có ít nhất 1 đoạn khớp chính xác 100% (0 lỗi)** với văn bản.
- Thuật toán sẽ dùng phiên bản tìm kiếm chính xác cực nhanh là **Boyer-Moore (sử dụng Bad Character Heuristic)** để tìm kiếm từng đoạn nhỏ này.
- Khi tìm thấy một đoạn nhỏ khớp chính xác tại một vị trí, ta lấy vị trí đó suy ngược ra vị trí bắt đầu dự kiến của toàn bộ pattern ban đầu (đây được gọi là một *Candidate* hay Ứng viên).
- Cuối cùng, ở **Bước xác minh (Verification Phase)**, thuật toán sẽ đối chiếu (verifiy) lại chuỗi pattern gốc tại từng vị trí Candidate. Nếu số lỗi thực sự $\le k$, kết quả đó được ghi nhận. Phương pháp này đóng vai trò như một bộ lọc (filter) cực kỳ hiệu quả.

## 2. Xác định Input / Output
- **Input:**
  - `text` (chuỗi): Chuỗi DNA gốc (genome hoặc sequence dài) cần tìm kiếm.
  - `pattern` (chuỗi): Chuỗi DNA mẫu cần tìm.
  - `k` (số nguyên): Số lượng ký tự sai lệch tối đa (mismatches) cho phép.
- **Output:**
  - `list[int]`: Danh sách vị trí các chỉ số (index) bắt đầu trong chuỗi `text` mà `pattern` có khớp (có sai lệch $\le k$).

## 3. Pseudocode (Mã giả)

```text
// Hàm phụ trợ Boyer-Moore tìm kiếm chính xác
Hàm BOYER_MOORE_EXACT(text, pattern):
    Tính bảng Bad_Character cho pattern
    results = []
    s = 0 (vị trí hiện tại trong text)
    Trong khi s <= len(text) - len(pattern):
        So sánh pattern với text từ phải qua trái
        Nếu khớp toàn bộ:
            Thêm s vào results
            Trượt s lên dựa theo luật Bad_Character
        Ngược lại:
            Trượt s lên dựa theo luật Bad_Character tại ký tự gây lỗi
    Trả về results

// Hàm chính: Boyer-Moore với Xác minh
Hàm BOYER_MOORE_WITH_VERIFICATION(text, pattern, k):
    Nếu k == 0:
        Trả về BOYER_MOORE_EXACT(text, pattern)
        
    num_segments = k + 1
    Chia pattern thành num_segments đoạn gần bằng nhau
    candidates = Set rỗng
    
    // Giai đoạn lọc (Filtering)
    Với mỗi đoạn p_i (từ chỉ số i):
        matches = BOYER_MOORE_EXACT(text, p_i)
        Với mỗi vị trí match trong matches:
            candidate_start = match - vị trí tương đối của p_i trong pattern
            Thêm candidate_start vào candidates
            
    // Giai đoạn xác minh (Verification)
    final_results = []
    Với mỗi cand trong candidates:
        mismatches = 0
        Với j từ 0 đến len(pattern) - 1:
            Nếu text[cand + j] != pattern[j]:
                mismatches = mismatches + 1
            Nếu mismatches > k:
                Thoát vòng lặp
        Nếu mismatches <= k:
            Thêm cand vào final_results
            
    Trả về final_results đã sắp xếp
```

## 4. Đánh giá độ phức tạp
- **Trường hợp tìm kiếm chính xác ($k=0$):**
  - Thời gian tiền xử lý: $O(M)$.
  - Thời gian tìm kiếm: Tốt nhất là $O(N/M)$ (nhờ bước nhảy lớn của Boyer-Moore), trung bình cực nhanh, tệ nhất là $O(N \cdot M)$. Với chuỗi DNA, kích thước bảng chữ cái nhỏ ($\Sigma=4$), luật Bad Character hoạt động tương đối tốt.
- **Trường hợp tìm kiếm xấp xỉ ($k > 0$):**
  - **Giai đoạn Filtering (lọc):** Chia pattern thành $k+1$ đoạn, độ dài mỗi đoạn $m \approx M/(k+1)$. Thuật toán Boyer-Moore chạy $k+1$ lần. Tổng thời gian tìm kiếm trung bình xấp xỉ $O(k \cdot N/m)$.
  - **Giai đoạn Verification (Xác minh):** Gọi $C$ là số lượng ứng viên (candidates) tiềm năng được sinh ra. Thời gian để xác minh tối đa là $O(C \cdot M)$. Trong thực tế, các đoạn ngắn sẽ dễ vô tình sinh ra nhiều ứng viên sai (false positives), nên bộ lọc này chỉ thực sự hiệu quả khi tỷ lệ lỗi $k/M$ nhỏ (tức là $M/(k+1)$ đủ lớn để ít sinh ra match ngẫu nhiên).
  - **Độ phức tạp tổng hợp thời gian:** $O(k \cdot \frac{N}{M/(k+1)} + C \cdot M)$.
  - **Độ phức tạp không gian (Space Complexity):** $O(M)$ để lưu trữ bảng Bad Character và các chuỗi con, cộng thêm $O(C)$ để lưu các vị trí ứng viên. Rất tiết kiệm RAM so với Suffix Tree.
