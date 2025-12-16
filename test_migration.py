import unittest
import pandas as pd
from migrate import transform_data

class TestETLProcess(unittest.TestCase):
    
    def setUp(self):
        """Création d'un mini jeu de données sale pour tester le nettoyage."""
        self.raw_data = pd.DataFrame({
            'Name': ['  bobby jackson  ', 'ALICE SMITH', 'John Doe'], # Test 1: Format Texte
            'Age': [30, 25, 40],
            'Gender': ['male', 'Female', 'Male'],
            'Date of Admission': ['2024-01-31', 'invalid-date', '2023-12-01'], # Test 2: Format Date
            'Medical Condition': ['Cancer', 'Flu', 'Cancer'],
            # Test 3 : Doublon (On va dupliquer une ligne manuellement dans le test)
        })

    def test_column_snake_case(self):
        """Test 1 : Vérifier que les colonnes sont bien renommées en snake_case"""
        df_clean = transform_data(self.raw_data)
        self.assertIn('date_of_admission', df_clean.columns)
        self.assertIn('medical_condition', df_clean.columns)
        self.assertNotIn('Date of Admission', df_clean.columns)

    def test_text_standardization(self):
        """Test 2 : Vérifier le format 'Title Case' et la suppression des espaces"""
        df_clean = transform_data(self.raw_data)
        self.assertEqual(df_clean.iloc[0]['name'], 'Bobby Jackson') # Était '  bobby jackson  '
        self.assertEqual(df_clean.iloc[1]['name'], 'Alice Smith')   # Était 'ALICE SMITH'

    def test_date_conversion(self):
        """Test 3 : Vérifier que les dates invalides deviennent NaT (Not a Time)"""
        df_clean = transform_data(self.raw_data)
        # La 2ème date était 'invalid-date', elle doit être NaT
        self.assertTrue(pd.isna(df_clean.iloc[1]['date_of_admission']))
        # La 1ère date doit être valide
        self.assertFalse(pd.isna(df_clean.iloc[0]['date_of_admission']))

    def test_duplicate_removal(self):
        """Test 4 : Vérifier la suppression des doublons"""
        # On crée un DF avec un doublon explicite
        df_with_dup = pd.concat([self.raw_data, self.raw_data.iloc[[0]]], ignore_index=True)
        self.assertEqual(len(df_with_dup), 4) # 3 + 1 doublon
        
        df_clean = transform_data(df_with_dup)
        self.assertEqual(len(df_clean), 3) # Le doublon doit avoir disparu

    def test_gender_consistency(self):
        """Test 5 : Vérifier l'uniformisation des catégories (ex: Gender)"""
        df_clean = transform_data(self.raw_data)
        unique_genders = df_clean['gender'].unique()
        self.assertIn('Male', unique_genders)
        self.assertIn('Female', unique_genders)
        self.assertNotIn('male', unique_genders) # Le minuscule ne doit plus exister

if __name__ == '__main__':
    unittest.main()