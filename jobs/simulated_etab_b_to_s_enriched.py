from pyspark.sql import SparkSession

# Création de la session Spark
spark = SparkSession.builder.appName("Enrichir_Etabs_avec_NAF_et_Clean").getOrCreate()

# === Lecture du fichier établissements (Silver) ===
etabs_path = "silver/simulated_etablissements_50000_b_to_s.csv"
etabs_df = spark.read.option("header", True).csv(etabs_path)

# === Lecture du fichier des intitulés NAF ===
naf_path = "int_courts_naf_rev_2.csv"
naf_df = spark.read.option("header", True).option("delimiter", ";").csv(naf_path)

# === Renommer les colonnes pour faciliter la jointure ===
naf_df = naf_df.withColumnRenamed("Code", "naf_code") \
               .withColumnRenamed("Intitulés de la  NAF rév. 2, version finale", "intitule_naf")

# === Jointure entre activitePrincipaleEtablissement et Code NAF ===
etabs_enriched = etabs_df.join(
    naf_df,
    etabs_df["activitePrincipaleEtablissement"] == naf_df["naf_code"],
    how="left"
)

# === Suppression des colonnes demandées ===
etabs_enriched = etabs_enriched.drop("activitePrincipaleEtablissement", "etatAdministratifEtablissement", "naf_code")

# === Sauvegarde du fichier enrichi ===
etabs_enriched.coalesce(1).write.mode("overwrite").option("header", True).csv("silver/simulated_etablissements_50000_b_to_s_enriched.csv")

print("✅ Fichier enrichi et nettoyé avec succès !")

# Arrêt de Spark
spark.stop()
