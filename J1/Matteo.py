import pandas as pd
df_customers = pd.read_csv("./dataset/customers.csv")
df_transactions = pd.read_csv("./dataset/transactions.csv")

df_customers_cleaned = df_customers[['first_purchase', 'last_purchase', 'country', 'customer_id']].drop_duplicates()
df_transactions_cleaned = df_transactions.drop_duplicates(subset=['invoice_date', 'quantity', 'unit_price', 'country', 'product_name', 'invoice_id'])

mapping_first = df_customers_cleaned[['first_purchase', 'country', 'customer_id']].rename(columns={'first_purchase': 'invoice_date'})
mapping_last = df_customers_cleaned[['last_purchase', 'country', 'customer_id']].rename(columns={'last_purchase': 'invoice_date'})
mapping = pd.concat([mapping_first, mapping_last]).drop_duplicates()

df_transactions_cleaned = df_transactions_cleaned.merge(mapping, on=['invoice_date', 'country'], how='left', suffixes=('', '_2'))
df_transactions_cleaned['customer_id'] = df_transactions_cleaned['customer_id'].fillna(df_transactions_cleaned['customer_id_2'])
df_transactions_cleaned.drop(columns=['customer_id_2'], inplace=True)

df_transactions_cleaned['customer_id'].isna().sum()

#Tentative de remplacement des customers id nuls sur les lignes de transaction en se faisant matcher last purchase/first purchase avec invoice_id et country avec country.
#Résultat : tentative infructueuse