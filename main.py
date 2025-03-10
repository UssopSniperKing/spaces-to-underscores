#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
from typing import Union, List

def replace_spaces_with_underscores(directory: Union[str, Path]) -> None:
    """
    Parcourt récursivement un répertoire et renomme tous les fichiers et 
    sous-répertoires en remplaçant les espaces par des underscores.
    
    Cette fonction utilise une approche en deux étapes pour éviter les problèmes
    de dépendances de chemin:
    1. D'abord, renomme tous les fichiers dans le répertoire actuel
    2. Ensuite, traite les sous-répertoires récursivement
    3. Finalement, renomme les sous-répertoires eux-mêmes
    
    Args:
        directory (Union[str, Path]): Le chemin du répertoire à traiter
            Peut être une chaîne de caractères ou un objet Path
    
    Returns:
        None: La fonction ne retourne rien mais affiche les actions effectuées
    """
    # Conversion en objet Path si nécessaire
    dir_path = Path(directory)
    
    # Liste tous les éléments dans le répertoire
    items: List[Path] = list(dir_path.iterdir())
    
    # ÉTAPE 1: Traite d'abord les fichiers
    for item_path in items:
        # Vérifie si c'est un fichier contenant des espaces
        if item_path.is_file() and ' ' in item_path.name:
            # Crée le nouveau nom
            new_name = item_path.name.replace(' ', '_')
            new_path = item_path.parent / new_name
            
            # Renomme le fichier
            item_path.rename(new_path)
            print(f"Fichier renommé: '{item_path}' -> '{new_path}'")
    
    # Récupère la liste mise à jour (après renommage des fichiers)
    updated_items: List[Path] = list(dir_path.iterdir())
    
    # ÉTAPE 2: Traite les sous-répertoires récursivement
    for item_path in updated_items:
        if item_path.is_dir():
            # Appel récursif pour traiter le contenu du sous-répertoire
            replace_spaces_with_underscores(item_path)
            
            # ÉTAPE 3: Renomme le sous-répertoire lui-même si nécessaire
            if ' ' in item_path.name:
                new_name = item_path.name.replace(' ', '_')
                new_path = item_path.parent / new_name
                
                # Renomme le répertoire
                item_path.rename(new_path)
                print(f"Répertoire renommé: '{item_path}' -> '{new_path}'")

def main() -> None:
    """
    Fonction principale du script.
    
    Parse les arguments de ligne de commande, vérifie la validité du répertoire
    spécifié et appelle la fonction de renommage principale.
    
    Returns:
        None
    """
    # Configuration du parser d'arguments
    parser = argparse.ArgumentParser(
        description="Renomme récursivement les fichiers et répertoires en remplaçant les espaces par des underscores."
    )
    parser.add_argument(
        "directory", 
        help="Chemin du répertoire à traiter"
    )
    
    # Parse les arguments
    args = parser.parse_args()
    
    # Conversion en objet Path
    directory = Path(args.directory)
    
    # Vérifie si le répertoire existe
    if not directory.is_dir():
        print(f"Erreur: '{directory}' n'est pas un répertoire valide.")
        sys.exit(1)
    
    # Convertit en chemin absolu pour plus de clarté dans les logs
    directory = directory.absolute()
    print(f"Traitement du répertoire: {directory}")
    
    # Exécute le renommage
    replace_spaces_with_underscores(directory)
    
    print("Opération terminée.")

if __name__ == "__main__":
    main()
