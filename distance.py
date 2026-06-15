from math import sqrt


def parse_point(point_str):
    if not point_str or not point_str.strip():
        raise ValueError("Le point ne peut pas etre vide")
    parts = point_str.strip().split(',')
    if len(parts) < 2:
        raise ValueError(f"Format invalide '{point_str}' : attendu 'x,y'")
    try:
        return tuple(float(c.strip()) for c in parts[:2])
    except ValueError:
        raise ValueError(f"Coordonnees invalides dans '{point_str}' : attendu des nombres")


def calculate_distance(point_a, point_b):
    return sqrt((point_b[0] - point_a[0])**2 + (point_b[1] - point_a[1])**2)
