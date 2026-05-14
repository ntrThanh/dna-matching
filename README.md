# DỰ ÁN DNA MATCHING

## Giới thiệu
Dự án này tập trung giải quyết bài toán **DNA Matching** bằng nhiều thuật toán tìm kiếm chuỗi khác nhau.

Mục tiêu chính:

- Cài đặt các thuật toán khớp chuỗi chính xác và gần đúng.
- So sánh hiệu năng của các thuật toán dựa trên thời gian chạy.
- Thực nghiệm trên cả dữ liệu nhân tạo và dữ liệu sinh học thực tế.

---

## Cấu trúc thư mục

```bash
DNA Matching/
│
├── dataset/
│   ├── artificial data/
│   │   ├── dna_10.txt
│   │   ├── dna_20.txt
│   │   ├── dna_40.txt
│   │   ├── dna_80.txt
│   │   ├── dna_160.txt
│   │   ├── dna_320.txt
│   │   ├── dna_640.txt
│   │   └── dna_1280.txt
│   │
│   ├── ncbi/
│       ├── data/
│       │   ├── GCF_000005845.2/
│       │   └── GCF_000008865.2/
│       │
│       ├── assembly_data_report.jsonl
│       ├── dataset_catalog.json
│       ├── ecoli_genomes.zip
│       ├── md5sum.txt
│       └── README.md
│
│   └── test cli/
│       └── test_cli/
│           ├── dna_exact.txt
│           ├── pattern_exact.txt
│           ├── dna_approx.txt
│           ├── pattern_approx.txt
│           ├── dna_long_2000.txt
│           └── pattern_long_k2.txt
│
├── experiments/
│   ├── mvtuong/
│   ├── ndtam/
│   ├── ntthanh/
│   └── nvtai/
│
├── base_class.py
├── generate_data.py
├── get_data.py
├── main.py
├── requirements.txt
└── README.md

```

## Cài đặt

Dự án chạy với Python 3. Cài các thư viện cần thiết bằng lệnh:

```bash
pip install -r requirements.txt
```

Các thuật toán chính trong `main.py` chỉ dùng thư viện chuẩn Python. `requirements.txt` chủ yếu phục vụ notebook thực nghiệm, vẽ biểu đồ và script lấy dữ liệu NCBI.

## Chạy bằng CLI

`main.py` nhận đầu vào là 2 file text riêng:

- File DNA gốc.
- File pattern cần tìm.

Mỗi file nên chỉ chứa chuỗi DNA. Nếu file ở dạng FASTA, các dòng bắt đầu bằng `>` sẽ được bỏ qua.

Cú pháp chung:

```bash
python3 main.py -t <file_dna> -p <file_pattern> -k <so_mismatch> -a <ten_thuat_toan>
```

Ví dụ chạy exact match:

```bash
python3 main.py -t "dataset/test cli/test_cli/dna_exact.txt" -p "dataset/test cli/test_cli/pattern_exact.txt" -k 0 -a brute_force
```

Ví dụ chạy approximate match với `k=1`:

```bash
python3 main.py -t "dataset/test cli/test_cli/dna_approx.txt" -p "dataset/test cli/test_cli/pattern_approx.txt" -k 1 -a kmp
```

Ví dụ chạy test case dài khoảng 2000 base:

```bash
python3 main.py -t "dataset/test cli/test_cli/dna_long_2000.txt" -p "dataset/test cli/test_cli/pattern_long_k2.txt" -k 2 -a boyer_moore
```

Với test case dài, kết quả kỳ vọng có match tại vị trí `900`.

Nếu chỉ muốn in danh sách vị trí match:

```bash
python3 main.py -t "dataset/test cli/test_cli/dna_long_2000.txt" -p "dataset/test cli/test_cli/pattern_long_k2.txt" -k 2 -a boyer_moore --matches-only
```

Các tên thuật toán hiện hỗ trợ:

- `brute_force`, alias: `bruteforce`, `bf`
- `rabin_karp`, alias: `rabinkarp`, `rk`
- `kmp`
- `boyer_moore`, alias: `boyermoore`, `bm`
- `suffix_array`, alias: `suffixarray`, `sa`
- `suffix_tree`, alias: `suffixtree`, `st`

Output mặc định là JSON:

```json
{
  "algorithm": "Boyer-Moore with Verification",
  "runtime_sec": 0.0012,
  "num_matches": 1,
  "matches": [900],
  "file_read_runtime_sec": 0.0028,
  "total_runtime_sec": 0.0040
}
```

Trong đó:

- `runtime_sec`: thời gian chạy thuật toán.
- `file_read_runtime_sec`: thời gian đọc file DNA và pattern.
- `total_runtime_sec`: tổng thời gian đọc file và chạy thuật toán.

## Chạy bằng code

Có thể import trực tiếp hàm trong `main.py`:

```python
from main import run_algorithm, run_algorithm_from_files

result = run_algorithm(
    text="GATACGA",
    pattern="GA",
    k=1,
    algorithm="kmp",
)

print(result)
```

Hoặc chạy từ file:

```python
from main import run_algorithm_from_files

result = run_algorithm_from_files(
    text_file="dataset/test cli/test_cli/dna_long_2000.txt",
    pattern_file="dataset/test cli/test_cli/pattern_long_k2.txt",
    k=2,
    algorithm="boyer_moore",
)

print(result)
```


## Hướng dẫn

Với mỗi thuật toán mà mọi người triển khai cần thực hiện phân tích bài toán, xác định in/output, pseudocode, độ phức tạp của thuật toán triển khai. Các thuật toán được sử dụng là: 
1. Brute Force with k mismatches
2. Rabin-Karp with verification
3. Bitap / Shift-Or
4. Dynamic Programming edit distance
5. Suffix Tree with backtracking
6. Suffix Array with candidate verification
7. Boyer-Moore with verification
8. KMP-based filtering + verification

Thư mục `experiments` là nơi các thành viên thực nghiệm các thuật toán của mình. Thực hiện Implement lại lớp `Algorithm` trong file `base_class.py` rồi thực nghiệm các thuật toán.

Thư mục `dataset` chứa dữ liệu thực nghiệm của bài toán trong đó có 2 loại dữ liệu là dữ liệu thực tế (mẫu DNA trên vi khuẩn Ecoli) và dữ liệu nhân tạo.

Thực hiện trước trên tập dữ liệu ban đầu, sau khi tất cả các thuật toán của mọi người hoạt động đúng thì thực hiện trên tập dữ liệu thực tế.
