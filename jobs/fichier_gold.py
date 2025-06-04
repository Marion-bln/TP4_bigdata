from pyspark.sql import SparkSession

# Création de la session Spark
spark = SparkSession.builder.appName("Etablissements_vers_Gold").getOrCreate()

# === Lecture des fichiers ===
enriched_path = "silver/simulated_etablissements_50000_b_to_s_enriched.csv/simu_etab_enriched.csv"
marchepub_path = "silver/marchepub_silver.csv/marchespub_silver.csv"

# Lecture des fichiers
df_enriched = spark.read.option("header", True).csv(enriched_path)
df_marchepub = spark.read.option("header", True).csv(marchepub_path)

# ✅ On renomme la colonne NAF longue tout de suite
df_enriched = df_enriched.withColumnRenamed("Intitulés de la  NAF rév. 2, version finale", "intitulé de la naf")

# Jointure sur le SIRET
df_gold = df_enriched.join(df_marchepub, on="siret", how="inner")

# Sélection des colonnes finales
df_gold = df_gold.select("siret","denomination_sociale", "adresse", "intitulé de la naf")

# Export final dans un seul fichier CSV
output_path = "gold/etablissements_gold.csv"
df_gold.coalesce(1).write.mode("overwrite").option("header", True).csv(output_path)

print("✅ Le fichier gold a bien été créé !")

spark.stop()
