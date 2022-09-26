import csv


class ReadAndWriteException(Exception):
    pass


class Writer(csv.DictWriter):    
    def __init__(self, filename, headers: list):
        self.filename = filename
        self.file = open(filename, "a+", newline="\n", encoding="utf-8")
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

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
    

class Reader(csv.DictReader):
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, "r", newline="\n", encoding="utf-8")
        super().__init__(self.file)
