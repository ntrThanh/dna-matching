# File này là file tôi sử dụng để lấy dữ liệu thử nghiệm, dữ liệu đã có sẵn rồi nên không cần chạy nữa!!
from Bio import Entrez, SeqIO

Entrez.email = "nguyentrongthanh672@gmail.com"

handle = Entrez.efetch(db="nucleotide", id="U00096", rettype="fasta", retmode="text")
record = SeqIO.read(handle, "fasta")
print(len(record.seq)) 
