from app import distances


class TestInterfaceHtml:
    """Tests d'interaction utilisateur via l'interface web (formulaire HTML)."""

    def test_get_affiche_le_formulaire(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'<form' in response.data

    def test_get_affiche_champ_point_a(self, client):
        response = client.get('/')
        assert b'point_a' in response.data

    def test_get_affiche_champ_point_b(self, client):
        response = client.get('/')
        assert b'point_b' in response.data

    def test_get_possede_des_labels(self, client):
        response = client.get('/')
        assert b'<label' in response.data

    def test_get_possede_un_bouton_soumettre(self, client):
        response = client.get('/')
        assert b'submit' in response.data

    def test_get_sans_resultat_au_chargement(self, client):
        response = client.get('/')
        assert 'Distance entre'.encode() not in response.data

    def test_post_exemple_du_sujet_a2_5_b1_6(self, client):
        # A(2,5) B(1,6) : sqrt((1-2)^2 + (6-5)^2) = sqrt(2) ~ 1.4142
        response = client.post('/', data={'point_a': '2,5', 'point_b': '1,6'})
        assert response.status_code == 200
        assert b'1.4142' in response.data

    def test_post_triple_pythagoricien_3_4_5(self, client):
        response = client.post('/', data={'point_a': '0,0', 'point_b': '3,4'})
        assert response.status_code == 200
        assert b'5.0000' in response.data

    def test_post_meme_point_distance_zero(self, client):
        response = client.post('/', data={'point_a': '7,3', 'point_b': '7,3'})
        assert response.status_code == 200
        assert b'0.0000' in response.data

    def test_post_coordonnees_negatives(self, client):
        # A(-1,-1) B(1,1) : sqrt(8) ~ 2.8284
        response = client.post('/', data={'point_a': '-1,-1', 'point_b': '1,1'})
        assert response.status_code == 200
        assert b'2.8284' in response.data

    def test_post_point_a_invalide_affiche_erreur(self, client):
        response = client.post('/', data={'point_a': 'abc', 'point_b': '1,6'})
        assert response.status_code == 200
        assert 'Erreur'.encode() in response.data

    def test_post_point_b_invalide_affiche_erreur(self, client):
        response = client.post('/', data={'point_a': '2,5', 'point_b': 'xyz'})
        assert response.status_code == 200
        assert 'Erreur'.encode() in response.data

    def test_post_champ_vide_affiche_erreur(self, client):
        response = client.post('/', data={'point_a': '', 'point_b': '1,6'})
        assert response.status_code == 200
        assert 'Erreur'.encode() in response.data

    def test_post_coordonnee_incomplete_affiche_erreur(self, client):
        # Seulement x sans y
        response = client.post('/', data={'point_a': '2', 'point_b': '1,6'})
        assert response.status_code == 200
        assert 'Erreur'.encode() in response.data

    def test_post_coordonnee_non_numerique_affiche_erreur(self, client):
        response = client.post('/', data={'point_a': '1,abc', 'point_b': '1,6'})
        assert response.status_code == 200
        assert 'Erreur'.encode() in response.data

    def test_post_valide_ajoute_dans_historique(self, client):
        client.post('/', data={'point_a': '0,0', 'point_b': '3,4'})
        assert len(distances) == 1

    def test_post_invalide_ne_modifie_pas_historique(self, client):
        client.post('/', data={'point_a': 'abc', 'point_b': '3,4'})
        assert len(distances) == 0
