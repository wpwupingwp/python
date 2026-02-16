import pandas as pd
from sys import argv
from pathlib import Path

filename = Path(argv[1])

data = pd.read_excel(filename)
a = data.iloc[:, 0]
b = data.iloc[:, 1]
a_jian_b = set(a.unique()) & set(b.unique())
out = pd.DataFrame(a_jian_b)
out.to_excel(filename.with_name("jiaoji.xls"))
