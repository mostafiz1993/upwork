import pandas as pd
th = [{'w' :1,'q' : 2}]
df1 = pd.DataFrame(th)
data = [{'a': df1, 'b': 2},{'a': 5, 'b': 10, 'c': 20}]
df = pd.DataFrame(data)
df.to_csv('test.csv')
print df