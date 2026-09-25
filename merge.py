import pandas as pd

df_clickhouse = pd.read_csv("schema_metadata.csv")
df_clickhouse["source_type"] = "clickhouse"

df_mysql_sl = pd.read_csv("schema_mysql.csv")
df_mysql_sl["source_type"] = "mysql-sl"

df_bigquery = pd.read_csv("schema_bigquery.csv")
df_bigquery["source_type"] = "bigquery"

df_unificado = pd.concat([df_clickhouse, df_mysql_sl, df_bigquery], ignore_index=True)

cols = ["source_type", "database_name", "table_name", "column_name", "column_position", "data_type", "is_nullable", "column_key"]
df_unificado = df_unificado[[c for c in cols if c in df_unificado.columns]]

df_unificado.to_csv("schema_metadata.csv", index=False)
print(f"✅ Catálogo consolidado exitosamente con {len(df_unificado)} registros.")