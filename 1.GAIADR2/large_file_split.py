
from fsplit.filesplit import FileSplit

# 90 Mb
max_size = 90 * 1000 * 1000
files = ("NGC2516.dat", "NGC2516_19.dat", "NGC2660.dat")

for file in files:
    fs = FileSplit(file=file, splitsize=max_size)
    fs.split()
