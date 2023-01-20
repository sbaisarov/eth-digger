import jsonlines


# class Writer(jsonlines.Writer):
#     def __init__(self, filename, mode="a+"):
#         self.filename = filename
#         self.file = open(filename, mode, newline="\n", encoding="utf-8")
#         super().__init__(self.file)

#     def to_address_list(self, key="address"):
#         self.file.seek(0)
#         wallets: list[str] = [row[key] for row in self.file.readlines()]
#         return wallets


class Reader(jsonlines.Reader):
    def __init__(self, filename, mode="r"):
        self.filename = filename
        self.file = open(filename, mode, newline="\n", encoding="utf-8")
        super().__init__(self.file)

    def __len__(self):
        counter = 0
        for _ in self.iter():
            counter += 1
        self.file.seek(0)
        return counter
