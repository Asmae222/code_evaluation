import pytest
from app import app, distances


@pytest.fixture(autouse=True)
def reset_distances():
    distances.clear()
    yield
    distances.clear()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# Interface HTML — interaction utilisateur via formulaire
# ---------------------------------------------------------------------------

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
        # Deux parties mais non numeriques : 'x,abc'
        response = client.post('/', data={'point_a': '1,abc', 'point_b': '1,6'})
        assert response.status_code == 200
        assert 'Erreur'.encode() in response.data

    def test_post_valide_ajoute_dans_historique(self, client):
        client.post('/', data={'point_a': '0,0', 'point_b': '3,4'})
        assert len(distances) == 1

    def test_post_invalide_ne_modifie_pas_historique(self, client):
        client.post('/', data={'point_a': 'abc', 'point_b': '3,4'})
        assert len(distances) == 0


# ---------------------------------------------------------------------------
# API REST — POST /api/distance
# ---------------------------------------------------------------------------

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
        # Deux parties mais non numeriques : '1,abc'
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


# ---------------------------------------------------------------------------
# API REST — GET /api/distances (historique)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Formule mathematique — theoreme de Pythagore
# ---------------------------------------------------------------------------

class TestFormuleDistance:
    """Verification de la formule mathematique (theoreme de Pythagore)."""

    def test_exemple_du_sujet(self, client):
        # A(2,5) B(1,6) -> sqrt(2) = 1.41421356...
        response = client.post('/api/distance',
                               json={'point_a': '2,5', 'point_b': '1,6'})
        assert response.get_json()['result_distance'] == pytest.approx(1.4142135623730951)

    def test_distance_horizontale(self, client):
        # Meme ordonnee -> distance = difference des abscisses
        response = client.post('/api/distance',
                               json={'point_a': '0,0', 'point_b': '5,0'})
        assert response.get_json()['result_distance'] == pytest.approx(5.0)

    def test_distance_verticale(self, client):
        # Meme abscisse -> distance = difference des ordonnees
        response = client.post('/api/distance',
                               json={'point_a': '0,0', 'point_b': '0,5'})
        assert response.get_json()['result_distance'] == pytest.approx(5.0)

    def test_symetrie_d_ab_egal_d_ba(self, client):
        r1 = client.post('/api/distance',
                         json={'point_a': '2,5', 'point_b': '1,6'}).get_json()
        r2 = client.post('/api/distance',
                         json={'point_a': '1,6', 'point_b': '2,5'}).get_json()
        assert r1['result_distance'] == pytest.approx(r2['result_distance'])

    def test_distance_origine(self, client):
        # A(0,0) B(1,1) -> sqrt(2)
        response = client.post('/api/distance',
                               json={'point_a': '0,0', 'point_b': '1,1'})
        assert response.get_json()['result_distance'] == pytest.approx(1.4142135623730951)
