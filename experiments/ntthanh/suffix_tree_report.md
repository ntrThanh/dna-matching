# Báo cáo Phân tích Thuật toán: Suffix Tree with Backtracking

## 1. Phân tích bài toán
Bài toán yêu cầu tìm kiếm tất cả các vị trí xuất hiện của một chuỗi mẫu (pattern) có độ dài $M$ bên trong một chuỗi văn bản (text) có độ dài $N$ (với $N$ rất lớn), cho phép sai lệch tối đa $k$ ký tự (mismatches).
Đối với bài toán DNA Matching:
- **Text ($T$)**: Là hệ gen (genome) hoặc đoạn DNA dài (vd: E.coli genome).
- **Pattern ($P$)**: Là đoạn DNA ngắn cần tìm.
- **k**: Số lượng đột biến/lỗi cho phép (mismatch).

Sử dụng **Suffix Tree (Cây hậu tố)** kết hợp với kỹ thuật **Backtracking (Quay lui)** cho phép duyệt toàn bộ các hậu tố của chuỗi gốc một cách tối ưu. Cây hậu tố cho phép chúng ta chia sẻ các tiền tố chung của các hậu tố, do đó tiết kiệm được không gian và thời gian khi so khớp mẫu với tập hợp hậu tố. Kỹ thuật Backtracking giúp ta rẽ nhánh để thử nghiệm các trường hợp có lỗi (mismatches) và quay lui nếu số lỗi vượt quá $k$.

## 2. Xác định Input / Output
- **Input:**
  - `text` (chuỗi): Chuỗi DNA gốc (genome hoặc sequence dài) cần tìm kiếm.
  - `pattern` (chuỗi): Chuỗi DNA mẫu cần khớp trong `text`.
  - `k` (số nguyên): Số lượng ký tự sai lệch tối đa cho phép.
- **Output:**
  - `list[int]`: Danh sách các chỉ số (index) bắt đầu trong chuỗi `text` nơi `pattern` khớp với số lỗi $\le k$.

## 3. Pseudocode (Mã giả)

```text
// 1. Khởi tạo và xây dựng cây hậu tố bằng thuật toán Ukkonen
Hàm BUILD_SUFFIX_TREE(text):
    Tree = Ukkonen_Algorithm(text + "$")
    Gọi DFS gán suffix_index cho tất cả các lá
    Trả về Tree

// 2. Tìm kiếm xấp xỉ có Quay lui
Hàm SEARCH_APPROX(Tree, pattern, k):
    Kết_quả = Tập_hợp_rỗng()
    
    Hàm DFS(node, pattern_idx, mismatches):
        Nếu mismatches > k:
            Trở về (Backtrack)
            
        Nếu pattern_idx == độ dài(pattern):
            Thêm tất cả các suffix_index dưới node vào Kết_quả
            Trở về
            
        Với mỗi (child_node) thuộc node.children:
            curr_p_idx = pattern_idx
            curr_mismatches = mismatches
            match_failed = Sai
            
            Với mỗi (char) trên cạnh đến child_node:
                Nếu curr_p_idx == độ_dài(pattern):
                    Thêm tất cả suffix_index của child_node vào Kết_quả
                    match_failed = Đúng
                    Thoát vòng lặp hiện tại
                
                Nếu char != pattern[curr_p_idx]:
                    curr_mismatches = curr_mismatches + 1
                    Nếu curr_mismatches > k:
                        match_failed = Đúng
                        Thoát vòng lặp hiện tại
                
                curr_p_idx = curr_p_idx + 1
                
            Nếu không match_failed:
                DFS(child_node, curr_p_idx, curr_mismatches)
                
    DFS(Tree.root, 0, 0)
    Trả về Kết_quả sắp xếp
```

## 4. Đánh giá độ phức tạp
- **Thời gian xây dựng (Time Complexity - Build):** $O(N)$ sử dụng thuật toán Ukkonen, với $N$ là độ dài của chuỗi `text`. Việc gán `suffix_index` (DFS) đi qua tất cả các node mất thời gian $O(N)$.
- **Thời gian tìm kiếm (Time Complexity - Search):**
  - Trong trường hợp khớp chính xác ($k=0$): $O(M + \text{occ})$, với $M$ là độ dài `pattern` và $\text{occ}$ là số lần xuất hiện.
  - Trong trường hợp xấp xỉ ($k>0$): Độ phức tạp tệ nhất phụ thuộc vào cấu trúc của cây và giá trị $k$, thường rơi vào $O(M \cdot \Sigma^k + \text{occ})$ hoặc $O(|V_k|)$ (với $|V_k|$ là số node được viếng thăm thỏa mãn điều kiện lỗi $\le k$). Tuy có thể lớn trong trường hợp tồi tệ, nhưng với $k$ nhỏ trên dữ liệu DNA, phương pháp này cắt tỉa nhánh (pruning) khá nhanh và hiệu quả hơn Brute Force.
- **Không gian (Space / Memory Complexity):**
  - $O(N \cdot |\Sigma|)$ đối với Suffix Trie, nhưng nhờ Suffix Tree kết nối các cạnh dài, số lượng node bị giới hạn ở $2N$.
  - Không gian lưu trữ trong thực tế của Cây hậu tố với Python khá lớn do đối tượng có nhiều thuộc tính (dictionary cho children), tỷ lệ khoảng $O(N)$ con trỏ. Tránh tràn Stack ở Python, thuật toán sử dụng phương pháp DFS Lặp (Iterative DFS) để thu thập kết quả thay vì đệ quy quá sâu.
