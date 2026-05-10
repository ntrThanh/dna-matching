import time


"""
Base class cho các thuật toán tìm kiếm chuỗi DNA. 
Các thuật toán cụ thể sẽ kế thừa lớp này và triển khai phương thức run().

Lớp này cũng cung cấp phương thức evaluate() để đo thời gian chạy và số lượng kết quả khớp.
"""
class Algorithm:
    def __init__(self, name = "BaseAlgorithm"):
        self.name = name

    def run(self, text, pattern, k=0):
        """
        Parameters
        ----------
        text : str
            Chuỗi DNA gốc (genome hoặc sequence dài) cần tìm kiếm.

        pattern : str
            Chuỗi DNA mẫu cần khớp trong text.

        k : int, optional
            Số lượng ký tự sai lệch tối đa cho phép giữa pattern
            và chuỗi con trong text (default = 0, tức khớp chính xác).

        Returns
        -------
        list[int]
            Danh sách các vị trí bắt đầu trong text mà pattern khớp
            với số sai lệch không vượt quá k.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def evaluate(self, text, pattern, k=0):
        start = time.perf_counter()

        result = self.run(text, pattern, k)

        end = time.perf_counter()
        runtime = end - start

        return {
            "algorithm": self.name,
            "runtime_sec": runtime,
            "num_matches": len(result),
            "matches": result
        }