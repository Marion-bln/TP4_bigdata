from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode

# Initialiser la session Spark
spark = SparkSession.builder.appName("Extract_Marches_Titulaires_Silver").getOrCreate()

# Lire le fichier JSON (utilise un chemin relatif ou absolu selon ton dossier)
df = spark.read.option("multiline", True).json("aws-marchespublics-annee-2022.json")

# Extraire la colonne "marches"
df_marches = df.select(explode("marches").alias("marche"))

# Exploser la liste de titulaires pour avoir une ligne par titulaire
df_titulaires = df_marches.select(explode("marche.titulaires").alias("titulaire"))

# Ne conserver que les colonnes id (siret) et denominationSociale
df_result = df_titulaires.select(
    col("titulaire.id").alias("siret"),
    col("titulaire.denominationSociale").alias("denomination_sociale")
).dropDuplicates(["siret"])

# Sauvegarder dans un seul fichier CSV nommé "marchepub_silver.csv"
output_path = "silver/marchepub_silver.csv"
df_result.coalesce(1).write.mode("overwrite").option("header", True).csv(output_path)

print("✅ Fichier 'marchepub_silver.csv' créé avec succès.")

spark.stop()


