import pandas as pd
import numpy as np

def electre_1(data, poids):
    # Normalisation des données
    normalized_data = data.copy()
    for column in poids.keys():
        normalized_data[column] = data[column] / np.sqrt((data[column]**2).sum())

    # Calcul de la matrice de concordance
    concordance_matrix = np.zeros((len(data), len(data)))
    for i in range(len(data)):
        for j in range(len(data)):
            concordance_matrix[i, j] = sum(
                poids[k] for k in poids if normalized_data.iloc[i][k] >= normalized_data.iloc[j][k]
            ) / sum(poids.values())

    # Calcul de la matrice de discordance
    discordance_matrix = np.zeros((len(data), len(data)))
    for i in range(len(data)):
        for j in range(len(data)):
            if i != j:
                if all(normalized_data.iloc[i][k] == normalized_data.iloc[j][k] for k in poids):
                    discordance_matrix[i, j] = 0  # Les alternatives sont équivalentes
                else:
                    discordance_matrix[i, j] = max(
                        (normalized_data.iloc[j][k] - normalized_data.iloc[i][k]) for k in poids if normalized_data.iloc[j][k] > normalized_data.iloc[i][k]
                    ) / max(
                        (max(normalized_data[k]) - min(normalized_data[k]) for k in poids)
                    )

    # Détermination des seuils de concordance et de discordance
    threshold_concordance = np.mean(concordance_matrix)
    threshold_discordance = np.mean(discordance_matrix)

    # Matrice de surclassement
    surclassement_matrix = np.zeros((len(data), len(data)))
    for i in range(len(data)):
        for j in range(len(data)):
            if i != j:
                if concordance_matrix[i, j] >= threshold_concordance and discordance_matrix[i, j] <= threshold_discordance:
                    surclassement_matrix[i, j] = 1

    return surclassement_matrix

def get_dominant_alternative(data, surclassement_matrix):
    # Compter le nombre de surclassements pour chaque alternative
    surclassement_counts = surclassement_matrix.sum(axis=1)

    # Trouver l'index de l'alternative dominante
    dominant_index = np.argmax(surclassement_counts)

    # Retourner l'alternative dominante
    return data.iloc[dominant_index]

# Charger les données à partir du fichier Excel
data = pd.read_excel("Meta-exemple-donnees_M1IT.xlsx")

# Définir les poids des critères
poids = {
    "Marque": 1,
    "Ecran": 1,
    "Caméra": 1,
    "Système": 1,
    "Matériau": 1,
    "Taille": 1,
    "Poids": 1,
    "Prix (€)": 1,
    "DAS": 1,
    "Processeur": 1,
    "RAM (GB)": 1,
    "Mémoire (GB)": 1,
    "Batterie": 1
}

# Vérifier que toutes les colonnes de poids sont présentes dans les données
for column in poids.keys():
    if column not in data.columns:
        raise ValueError(f"La colonne '{column}' n'est pas présente dans les données.")

# Calculer la matrice de surclassement
surclassement_matrix = electre_1(data, poids)

# Obtenir l'alternative dominante
dominant_alternative = get_dominant_alternative(data, surclassement_matrix)

# Afficher l'alternative dominante
print("Meilleur choix de téléphone portable :")
print(dominant_alternative)
