import pytest
from app import distances


class TestApiCalculDistance:
    """Tests de l'endpoint de calcul via l'API REST."""

    def test_post_valide_retourne_201(self, client):
        response = client.post('/api/distance',
                               json={'point_a': '2,5', 'point_b': '1,6'})
        assert response.status_code == 201

    def test_post_valide_retourne_distance_correcte(self, client):
        response = client.post('/api/distance',
                               json={'point_a': '0,0', 'point_b': '3,4'})
        assert response.get_json()['result_distance'] == pytest.approx(5.0)

    def test_post_valide_retourne_point_a(self, client):
        response = client.post('/api/distance',
                               json={'point_a': '2,5', 'point_b': '1,6'})
        assert response.get_json()['point_a'] == [2.0, 5.0]

    def test_post_valide_retourne_point_b(self, client):
        response = client.post('/api/distance',
                               json={'point_a': '2,5', 'point_b': '1,6'})
        assert response.get_json()['point_b'] == [1.0, 6.0]

    def test_post_valide_retourne_horodatage(self, client):
        response = client.post('/api/distance',
                               json={'point_a': '0,0', 'point_b': '1,1'})
        assert 'requested_at' in response.get_json()

    def test_post_sans_corps_json_retourne_400(self, client):
        response = client.post('/api/distance')
        assert response.status_code == 400

    def test_post_point_a_invalide_retourne_400(self, client):
        response = client.post('/api/distance',
                               json={'point_a': 'invalide', 'point_b': '1,6'})
        assert response.status_code == 400

    def test_post_coordonnee_non_numerique_retourne_400(self, client):
        response = client.post('/api/distance',
                               json={'point_a': '1,abc', 'point_b': '1,6'})
        assert response.status_code == 400

    def test_post_point_b_invalide_retourne_400(self, client):
        response = client.post('/api/distance',
                               json={'point_a': '2,5', 'point_b': 'mauvais'})
        assert response.status_code == 400

    def test_post_point_a_manquant_retourne_400(self, client):
        response = client.post('/api/distance', json={'point_b': '1,6'})
        assert response.status_code == 400

    def test_post_point_b_manquant_retourne_400(self, client):
        response = client.post('/api/distance', json={'point_a': '2,5'})
        assert response.status_code == 400

    def test_post_reponse_erreur_contient_message(self, client):
        response = client.post('/api/distance',
                               json={'point_a': 'nope', 'point_b': '1,6'})
        assert 'error' in response.get_json()

    def test_get_non_autorise_retourne_405(self, client):
        response = client.get('/api/distance')
        assert response.status_code == 405

    def test_put_non_autorise_retourne_405(self, client):
        response = client.put('/api/distance',
                              json={'point_a': '0,0', 'point_b': '1,1'})
        assert response.status_code == 405

    def test_post_valide_ajoute_dans_historique(self, client):
        client.post('/api/distance', json={'point_a': '0,0', 'point_b': '3,4'})
        assert len(distances) == 1


class TestApiHistorique:
    """Tests de l'historique des calculs."""

    def test_historique_initialement_vide(self, client):
        response = client.get('/api/distances')
        assert response.status_code == 200
        assert response.get_json() == []

    def test_calcul_api_apparait_dans_historique(self, client):
        client.post('/api/distance', json={'point_a': '0,0', 'point_b': '3,4'})
        data = client.get('/api/distances').get_json()
        assert len(data) == 1
        assert data[0]['result_distance'] == pytest.approx(5.0)

    def test_calcul_html_apparait_dans_historique(self, client):
        client.post('/', data={'point_a': '0,0', 'point_b': '3,4'})
        data = client.get('/api/distances').get_json()
        assert len(data) == 1

    def test_historique_accumule_plusieurs_calculs(self, client):
        client.post('/api/distance', json={'point_a': '0,0', 'point_b': '1,0'})
        client.post('/api/distance', json={'point_a': '0,0', 'point_b': '0,1'})
        client.post('/', data={'point_a': '0,0', 'point_b': '1,1'})
        assert len(client.get('/api/distances').get_json()) == 3

    def test_post_sur_distances_non_autorise(self, client):
        response = client.post('/api/distances')
        assert response.status_code == 405

    def test_historique_contient_horodatage(self, client):
        client.post('/api/distance', json={'point_a': '0,0', 'point_b': '1,0'})
        data = client.get('/api/distances').get_json()
        assert 'requested_at' in data[0]
