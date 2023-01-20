import csv
import sys

csv.field_size_limit(sys.maxsize)  # the limited amount of rows is not enough


class Writer(csv.DictWriter):
    def __init__(self, filename, headers: list[str] = [], mode="a+"):
        self.filename = filename
        self.file = open(filename, mode, newline="\n", encoding="utf-8")
        super().__init__(self.file, headers)
        if self.file.tell() == 0:
            super().writeheader()

    def to_address_list(self, key="address"):
        self.file.seek(0)
        reader = csv.DictReader(self.file)
        wallets: list[str] = []
        for row in reader:
            wallets.append(row[key])
        return wallets

    def close(self):
        self.file.close()


class Reader(csv.DictReader):
    def __init__(self, filename, fieldnames: list[str] = [], mode="r"):
        self.filename = filename
        self.file = open(filename, mode, newline="\n", encoding="utf-8")
        super().__init__(self.file, fieldnames=fieldnames)

    def close(self):
        self.file.close()

    def __len__(self):
        length = len([row for row in self])
        self.file.seek(0)
        next(self)  # skip header
        return length
