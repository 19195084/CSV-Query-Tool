# CSV Query Tool :outbox_tray:

Outil de filtrage CSV avancé avec syntaxe de type SQL

## Fonctionnalités

- Filtrage complexe avec opérateurs logiques
- Support des expressions régulières
- Gestion des valeurs nulles et vides
- Validation des valeurs via fichier JSON
- Export des résultats en CSV
- Sélection de colonnes spécifiques

## Installation

### Création de l'environnement virtuel

```bash
# Sous Linux/macOS:
python3 -m venv env
source env/bin/activate

# Sous Windows:
python -m venv env
env\Scripts\activate
```

### Installation des dépendances

```bash
pip install pandas numpy
```

## Utilisation de base

```bash
python csv_query.py \
  --input input.csv \
  --output results.csv \
  --status-config status.json \
  --query "age > 30" \
  --fields nom,email,age
```

## Syntaxe des filtres

### Opérateurs de comparaison
| Opérateur | Exemple                     | Description                      |
|-----------|-----------------------------|----------------------------------|
| `=`       | `status = 'actif'`          | Égalité stricte                 |
| `!=`      | `ville != 'Paris'`          | Différent                       |
| `>`, `<`  | `age > 25`                  | Comparaison numérique           |
| `>=`, `<=`| `salaire >= 3000`           | Comparaison numérique           |
| `LIKE`    | `nom LIKE 'A%'`             | Pattern matching                |
| `IN`      | `ville IN ('Paris,Lyon')`   | Liste de valeurs                |
| `IS NULL` | `email IS NULL`             | Valeurs manquantes              |
| `NOT`     | `NOT status = 'inactif'`    | Négation logique                |

### Combinaisons logiques
```bash
--query "(age > 18 AND status = 'actif') OR newsletter = True"
--query "departement = 'IT' AND (salaire > 5000 OR anciennete > 5)"
```

### Filtres sur texte
```bash
--query "nom.str.startswith('A')"
--query "email.str.contains('@gmail.com', case=False)"
--query "telephone.str.match('^\\+33')"
--query "nom.str.len() > 10"
```

### Filtres sur dates
```bash
--query "date_naissance.dt.year > 2000"
--query "'2023-01-01' < date_embauche <= '2023-12-31'"
--query "date_commande.dt.dayofweek == 0"
```

### Filtres avancés
```bash
--query "revenu_brut - revenu_net > 1000"
--query "telephone.isnull() & email.notnull()"
--query "id_employe in [123, 456, 789]"
--query "(votes_positifs / (votes_positifs + votes_negatifs)) > 0.7"
```

## Configuration des statuts

Format du fichier `status.json` :
```json
{
  "statut": ["actif", "inactif", "en_attente", "en_conge"]
}
```

## Gestion des erreurs

### Exemples d'erreurs courantes
```bash
Error: Statut(s) invalide(s) : ['invalid_status']. Statuts autorisés : ['actif', 'inactif']
Error: "Colonnes manquantes : {'colonne_inexistante'}"
Error: "Failed to parse query"
```

## Bonnes pratiques

1. **Encadrer les chaînes par des apostrophes** :
   ```bash
   --query "ville == 'Paris'"
   ```
2. **Utiliser les parenthèses pour les priorités** :
   ```bash
   --query "(A OR B) AND C"
   ```
3. **Vérifier les types de données** :
   ```bash
   --query "is_active == True"
   ```
4. **Optimiser les performances** :
   ```bash
   --query "categorie == 'A' & quantite > 10"
   ```

## Cas complexes

### Filtre temporel combiné
```bash
--query "date_vente.between('2023-01-01', '2023-03-31') and (produit == 'ordinateur' or produit == 'telephone') and taux_remise > 0.2"
```

### Analyse de texte avancée
```bash
--query "email.str.match('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')"
--query "adresse.str.contains('\\d{5}')"
```

### Agrégations conditionnelles
```bash
--query "salaire > salaire.quantile(0.9)"
```

## Options complètes

| Option            | Description                               |
|-------------------|-------------------------------------------|
| `--input`         | Fichier CSV d'entrée (obligatoire)        |
| `--output`        | Fichier CSV de sortie (obligatoire)       |
| `--query`         | Requête de filtrage (optionnel)           |
| `--fields`        | Colonnes à exporter (séparées par virgules) |
| `--status-config` | Fichier JSON de configuration des statuts |
| `--help`          | Affiche l'aide                            |

