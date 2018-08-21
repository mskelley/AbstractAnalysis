import pandas as pd

def load_pnas(file_name, encoding='utf8', delimiter='|'):
	return pd.read_csv(file_name, header=0, sep=delimiter, encoding=encoding)