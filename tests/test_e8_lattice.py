"""Verification tests for the pure E8 lattice core.

The tests assert standard coordinate-model properties.  They deliberately do
not attach any governance or symbolic meaning to E8; that belongs to a later,
separately ratified experiment.
"""

import random
import sys
from itertools import product
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from topologies.e8_lattice import (
    COVERING_RADIUS_SQUARED,
    DIMENSION,
    first_shell,
    is_lattice_point,
    nearest_point,
    quantization_error_squared,
    shell_index,
    squared_norm,
)


def _distance_squared(left, right):
    return sum((a - b) ** 2 for a, b in zip(left, right))


class TestE8Membership:
    def test_integer_coset_requires_even_coordinate_sum(self):
        assert is_lattice_point((1, 1, 0, 0, 0, 0, 0, 0))
        assert is_lattice_point((2, 0, 0, 0, 0, 0, 0, 0))
        assert not is_lattice_point((1, 0, 0, 0, 0, 0, 0, 0))

    def test_half_integer_coset_requires_even_coordinate_sum(self):
        # All +1/2 coordinates sum to 4, which is even.
        assert is_lattice_point((0.5,) * DIMENSION)
        # One negative half gives coordinate sum 3, which is odd.
        assert not is_lattice_point((-0.5,) + (0.5,) * 7)

    def test_mixed_coordinate_classes_are_not_lattice_points(self):
        assert not is_lattice_point((0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

    def test_membership_rejects_wrong_dimension(self):
        with pytest.raises(ValueError):
            is_lattice_point((0.0,) * 7)


class TestFirstShell:
    def test_first_shell_has_exactly_240_roots(self):
        assert len(first_shell()) == 240
        assert len(set(first_shell())) == 240

    def test_every_root_is_an_e8_member_with_squared_norm_two(self):
        for root in first_shell():
            assert is_lattice_point(root)
            assert squared_norm(root) == pytest.approx(2.0)
            assert shell_index(root) == 1

    def test_root_family_counts_match_coordinate_construction(self):
        roots = first_shell()
        integer_roots = [
            root for root in roots if all(value.is_integer() for value in root)
        ]
        half_roots = [root for root in roots if root not in integer_roots]
        assert len(integer_roots) == 112
        assert len(half_roots) == 128


class TestNearestPointDecoder:
    def test_decoder_returns_lattice_member_and_is_idempotent(self):
        vectors = (
            (0.1, -0.4, 0.7, 1.3, -1.2, 2.4, -2.6, 0.5),
            (0.5,) * DIMENSION,
            (1.1, 0.9, 0.1, -0.1, 0.2, -0.2, 0.4, -0.4),
        )
        for vector in vectors:
            point = nearest_point(vector)
            assert is_lattice_point(point)
            assert nearest_point(point) == point

    def test_decoder_matches_brute_force_first_shell_near_a_root(self):
        roots = first_shell()
        root = roots[37]
        perturbation = (0.031, -0.021, 0.014, -0.009, 0.025, -0.017, 0.012, -0.008)
        vector = tuple(value + delta for value, delta in zip(root, perturbation))
        brute_force = min(roots, key=lambda candidate: _distance_squared(vector, candidate))
        assert nearest_point(vector) == brute_force

    def test_quantization_error_is_bounded_by_e8_covering_radius(self):
        rng = random.Random(26397)
        for _ in range(250):
            vector = tuple(rng.uniform(-10.0, 10.0) for _ in range(DIMENSION))
            assert quantization_error_squared(vector) <= COVERING_RADIUS_SQUARED + 1e-12

    def test_decoder_is_stable_inside_one_local_cell(self):
        root = first_shell()[0]
        perturbations = product((-0.02, 0.0, 0.02), repeat=DIMENSION)
        # A small structured subset of the local cube is sufficient to show
        # stability without relying on random samples.
        for index, perturbation in enumerate(perturbations):
            if index >= 81:
                break
            vector = tuple(value + delta for value, delta in zip(root, perturbation))
            assert nearest_point(vector) == root


class TestShellIndex:
    def test_shell_index_for_origin_and_first_shell(self):
        assert shell_index((0.0,) * DIMENSION) == 0
        assert shell_index(first_shell()[0]) == 1

    def test_shell_index_rejects_non_lattice_vectors(self):
        with pytest.raises(ValueError):
            shell_index((0.1,) * DIMENSION)
