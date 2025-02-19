import argparse
import pandas as pd
import numpy as np
import json
import re

class CSVFilter:
    def __init__(self, csv_path, status_config):
        self.df = pd.read_csv(csv_path)
        with open(status_config) as f:
            self.allowed_status = json.load(f).get('statut', [])
        
    def validate_status(self, query):
        # Extraction des valeurs de statut utilisées
        status_values = set()
        patterns = [
            r"status\s*==\s*'([^']+)'",
            r"status\s*!=\s*'([^']+)'",
            r"status\s+in\s*\(([^)]+)\)",
            r"status\s+not in\s*\(([^)]+)\)"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                if ',' in match:
                    status_values.update([v.strip("' ") for v in match.split(',')])
                else:
                    status_values.add(match.strip("' "))
        
        # Validation
        invalid = [v for v in status_values if v not in self.allowed_status]
        if invalid:
            raise ValueError(f"Statut(s) invalide(s) : {invalid}. Statuts autorisés : {self.allowed_status}")

    def apply_query(self, query):
        # Conversion des opérateurs SQL-like
        query = re.sub(r'\bLIKE\s+"%(.+)%"', r'.str.contains("\1")', query)
        query = re.sub(r'\bLIKE\s+"(.+)%"', r'.str.startswith("\1")', query)
        query = re.sub(r'\bLIKE\s+"%(.+)"', r'.str.endswith("\1")', query)
        query = re.sub(r'\bIS NULL\b', r'.isnull()', query)
        query = re.sub(r'\bNOT NULL\b', r'.notnull()', query)
        
        return self.df.query(query, engine='python')

def main():
    parser = argparse.ArgumentParser(description="Filtre CSV avancé avec syntaxe de type SQL")
    parser.add_argument('--input', required=True, help='Fichier CSV en entrée')
    parser.add_argument('--output', required=True, help='Fichier CSV en sortie')
    parser.add_argument('--query', help="Requête de filtrage (ex: \"age > 30 and status == 'actif' or nom.str.contains('^A')\")")
    parser.add_argument('--fields', help='Colonnes à exporter (séparées par des virgules)')
    parser.add_argument('--status-config', required=True, help='Fichier JSON de configuration des statuts')
    
    args = parser.parse_args()
    
    filter = CSVFilter(args.input, args.status_config)
    
    if args.query:
        filter.validate_status(args.query)
        result = filter.apply_query(args.query)
    else:
        result = filter.df
    
    if args.fields:
        columns = [c.strip() for c in args.fields.split(',')]
        missing = set(columns) - set(result.columns)
        if missing:
            raise ValueError(f"Colonnes manquantes : {missing}")
        result = result[columns]
    
    result.to_csv(args.output, index=False)

if __name__ == '__main__':
    main()
