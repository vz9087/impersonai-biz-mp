import pandas as pd
df = pd.read_csv('data/training_data.csv')
print(f"Total:     {len(df)}")
print(f"Legit:     {(df.label==0).sum()}")
print(f"Malicious: {(df.label==1).sum()}")
print(f"Ratio:     {(df.label==0).sum() / len(df) * 100:.1f}% legit")