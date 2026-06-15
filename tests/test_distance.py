import pytest
from distance import parse_point, calculate_distance


class TestParsePoint:
    """Tests unitaires de la fonction parse_point."""

    def test_point_valide_retourne_tuple(self):
        assert parse_point('2,5') == (2.0, 5.0)

    def test_point_flottant_valide(self):
        assert parse_point('1.5,2.7') == (1.5, 2.7)

    def test_point_negatif_valide(self):
        assert parse_point('-1,-1') == (-1.0, -1.0)

    def test_point_avec_espaces_valide(self):
        assert parse_point('2 , 5') == (2.0, 5.0)

    def test_point_vide_leve_erreur(self):
        with pytest.raises(ValueError):
            parse_point('')

    def test_point_espace_seul_leve_erreur(self):
        with pytest.raises(ValueError):
            parse_point('   ')

    def test_point_incomplet_leve_erreur(self):
        # Seulement x sans y
        with pytest.raises(ValueError):
            parse_point('2')

    def test_point_non_numerique_leve_erreur(self):
        with pytest.raises(ValueError):
            parse_point('abc,def')

    def test_point_partiellement_numerique_leve_erreur(self):
        with pytest.raises(ValueError):
            parse_point('1,abc')


class TestCalculDistance:
    """Tests unitaires de la fonction calculate_distance."""

    def test_exemple_du_sujet(self):
        # A(2,5) B(1,6) -> sqrt(2)
        assert calculate_distance((2, 5), (1, 6)) == pytest.approx(1.4142135623730951)

    def test_triple_pythagoricien_3_4_5(self):
        assert calculate_distance((0, 0), (3, 4)) == pytest.approx(5.0)

    def test_distance_zero_meme_point(self):
        assert calculate_distance((3, 3), (3, 3)) == pytest.approx(0.0)

    def test_distance_horizontale(self):
        # Meme ordonnee -> distance = difference des abscisses
        assert calculate_distance((0, 0), (5, 0)) == pytest.approx(5.0)

    def test_distance_verticale(self):
        # Meme abscisse -> distance = difference des ordonnees
        assert calculate_distance((0, 0), (0, 5)) == pytest.approx(5.0)

    def test_symetrie_ab_egal_ba(self):
        assert calculate_distance((2, 5), (1, 6)) == pytest.approx(
            calculate_distance((1, 6), (2, 5))
        )

    def test_coordonnees_negatives(self):
        # A(-1,-1) B(1,1) -> sqrt(8) ~ 2.8284
        assert calculate_distance((-1, -1), (1, 1)) == pytest.approx(2.8284271247461903)
