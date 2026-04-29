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
│   └── ncbi/
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
├── experiments/
│   ├── mvtuong/
│   ├── ndtam/
│   ├── ntthanh/
│   └── nvtai/
│
├── base_class.py
├── generate_data.py
├── get_data.py
└── README.md

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

