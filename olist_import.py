import yaml, glob
import pandas as pd
from sqlalchemy import create_engine

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
#print(config)
engine = create_engine(config['olist'])

print('reche des fichiers : '+config['olist_csv']+"/*.csv")
fns = glob.glob(config['olist_csv']+"/*.csv")

dtype = {'customer_zip_code_prefix': str, 'geolocation_zip_code_prefix': str, 'seller_zip_code_prefix': str}

# Import des CSV vers PG
for fn in fns:
    tbl=fn[35:-4].replace("_dataset", "")
    df = pd.read_csv(fn, dtype=dtype)
    print(f"- {fn} : {tbl}, {df.shape}")
    print(df.dtypes)
    df.to_sql(tbl, engine, if_exists='replace', index=False)