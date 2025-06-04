from pyspark.sql import SparkSession
from pyspark.sql.functions import concat_ws, col
import os

# Créer la session Spark
spark = SparkSession.builder \
    .appName("Etablissements_Bronze_To_Silver") \
    .getOrCreate()

# Lire les données
df = spark.read.option("header", True).csv("simulated_etablissements_50000.csv")

# Filtrer les établissements actifs
df_active = df.filter(col("etatAdministratifEtablissement") == "A")

# Colonnes utiles
colonnes_utiles = [
    "siret", "activitePrincipaleEtablissement",
    "etatAdministratifEtablissement", "libelleCommuneEtablissement",
    "codePostalEtablissement", "libelleVoieEtablissement",
    "numeroVoieEtablissement", "typeVoieEtablissement",
    "complementAdresseEtablissement"
]

df_selected = df_active.select(*colonnes_utiles)

# Création de la colonne "adresse"
df_adresse = df_selected.withColumn(
    "adresse",
    concat_ws(" ",
        col("numeroVoieEtablissement"),
        col("typeVoieEtablissement"),
        col("libelleVoieEtablissement"),
        col("libelleCommuneEtablissement"),
        col("codePostalEtablissement"),
        col("complementAdresseEtablissement")
    )
)

# Supprimer les colonnes individuelles utilisées pour l'adresse
colonnes_a_supprimer = [
    "numeroVoieEtablissement", "typeVoieEtablissement",
    "libelleVoieEtablissement", "libelleCommuneEtablissement",
    "codePostalEtablissement", "complementAdresseEtablissement"
]

df_final = df_adresse.drop(*colonnes_a_supprimer)

# Sauvegarde en un seul fichier CSV
output_path = "silver/simulated_etablissements_50000_b_to_s.csv"
df_final.coalesce(1).write.mode("overwrite").option("header", True).csv(output_path)



print("✅ Données enregistrées sans les colonnes d’adresse détaillées.")




