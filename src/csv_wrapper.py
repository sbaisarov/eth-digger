import csv
import sys


csv.field_size_limit(sys.maxsize)


class ReadAndWriteException(Exception):
    pass


class Writer(csv.DictWriter):
    def __init__(self, filename, headers: list, mode="w"):
        self.filename = filename
        self.file = open(filename, mode, newline="\n", encoding="utf-8")
        super().__init__(self.file, headers)
        if self.file.tell() == 0:
            super().writeheader()

    def to_list(self):
        self.file.seek(0)
        reader = csv.DictReader(self.file)
        wallets = []
        for row in reader:
            wallet = row["account"]
            wallets.append(wallet)
        return wallets

    def close(self):
        self.file.close()


class Reader(csv.DictReader):
    def __init__(self, filename, fieldnames=None):
        self.filename = filename
        self.file = open(filename, "r", newline="\n", encoding="utf-8")
        super().__init__(self.file, fieldnames=fieldnames)

    def close(self):
        self.file.close()

    def __len__(self):
        length = len([row for row in self])
        self.file.seek(0)
        next(self)  # skip header
        return length
