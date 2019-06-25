
import pytest
import numpy as np
from nautilus_nlp.preprocessing.preprocess import fix_bad_unicode



@pytest.mark.parametrize(
    "input_str, expected_str",
    [
    ('Les augmentations de rÃ©munÃ©rations',
  'Les augmentations de rémunérations'),
 ("rÃ©nover l'enquÃªte publique pour en faire un vrai outil  d'amÃ©nagement du territoire et de dialogue social",
  "rénover l'enquête publique pour en faire un vrai outil  d'aménagement du territoire et de dialogue social"),
 ('Limitations de vitesse et sÃ©curitÃ© routiÃ¨re',
  'Limitations de vitesse et sécurité routière'),
 ('Pour un nouveau contrat citoyen', 'Pour un nouveau contrat citoyen'),
 ('DÃ©velopper les dÃ©marches de budget participatif dans les collectivitÃ©s et associer les citoyens dans la rÃ©alisation des projets',
  'Développer les démarches de budget participatif dans les collectivités et associer les citoyens dans la réalisation des projets'),
 ('proportienelle', 'proportienelle'),
 ('Pour plus de dÃ©mocratie participative',
  'Pour plus de démocratie participative'),
 ('Transparence de la vie public', 'Transparence de la vie public'),
 ('18 mois de trop....ca suffit macron',
  '18 mois de trop....ca suffit macron'),
 ('EgalitÃ© devant les infractions routiÃ¨res',
  'Egalité devant les infractions routières')
    ],
)
def test_remove_multiple_spaces_and_strip_text(input_str, expected_str):
    result = fix_bad_unicode(input_str)
    np.testing.assert_string_equal(result, expected_str)