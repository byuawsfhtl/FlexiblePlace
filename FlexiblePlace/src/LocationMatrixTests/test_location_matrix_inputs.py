import unittest
from FlexiblePlace.src.LocationMatrix import LocationMatrix
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace


class TestLocationMatrixInputsFromOtherTests(unittest.TestCase):
    """Create LocationMatrix instances for the various inputs used in the compare/combiner tests
    to make sure LocationMatrix accepts and arranges them without immediate errors."""

    def setUp(self):
        # Pairs and groups taken from test_compare_places.py and test_combine_flexible_places.py
        self.pairs = [
            ("", ""),
            ("Paterson, Passaic, New Jersey, United States", ""),
            ("", "Paterson, Passaic, New Jersey, United States"),
            ("Belgium", "Belgium"),
            ("Camden, New Jersey, United States", "Camden, Camden, New Jersey, United States"),
            ("No Croghan J*, New York, United States", "New York, United States"),
            ("   ", "   "),
            ("Houston, Texas", "Houston, Harris, Texas, United States"),
        ]

        self.groups = [
            # from combine tests: small examples and some with outliers
            ["Belgium"],
            ["Belgium", "Belgium"],
            ["Paris", "Belgium"],
            ["Melgium", "Belgium"],
            ["Camden, New Jersey",
             "Camden, Camden, New Jersey, United States",
             "reallylongcityname, reallylongcountyname, reallylongstatename, reallylongcountryname"],
            ["New York, New York, United States",
             "New York, United States",
             "reallylongcityname, reallylongstatename, UnitedStates"],
            ["Lawrence, Massachusetts, United States",
             "Lawrence, Essex, Massachusetts, United States"],
            ["Buffalo, New York, United States",
             "Buffalo, Erie, New York"],
            ["Springfield, Sangamon, Illinois",
             "Springfield, Illinois, United States",
             "reallylongcityname, Sangamon, Illinois, United States"],
            ["Phila, Pennsylvania, United States",
             "Philadelphia, Pennsylvania"],
            ["Elder Twp, Pennsylvania, United States",
             "Elder Township, Cambria, Pennsylvania"],
            ["Elder Twp, Pennsylvania, United States",
             "Elder Township, Cambria, Pennsylvania",
             "reallylongcityname, Pennsylvania, United States"],
            ["Phila, Pennsylvania, United States",
             "Philadelphia Monthly Meeting, Philadelphia, Philadelphia, Pennsylvania"],
            ["Sugarloaf Township, Pennsylvania, United States",
             "Luzerne, Pennsylvania",
             "Sugarloaf Township, Luzerne, Pennsylvania"],
            ["Paris, France",
             "Paris, Texas",
             "Texas, United States"],
            ["New York, Iowa, United States",
             "New York, United States",
             "New York, New York, United States"],
            ["Washington, Utah",
             "Walla Walla, Washington",
             "Washington, United States"],
            ["United States",
             "Belgium",
             "Washington, Utah",
             "Walla Walla, Washington",
             "Washington, United States"],
            ["Massachusetts Bay Colony, British Colonial America",
             "British Colonial America",
             "Lincoln, Massachusetts Bay Colony",
             "Bucksport, Lincoln, Massachusetts Bay Colony",
             "Lincoln, Massachusetts Bay Colony, British Colonial America",
             "reallysuperlongcityname, reallysuperlongcountyname, reallysuperlongstatename, reallysuperlongcountryname",
             "Belgium"]
        ]

    def test_pairs_construct_ok(self):
        """Construct matrices for all pair inputs used in compare tests without exception and with correct sizes"""
        for a, b in self.pairs:
            with self.subTest(a=a, b=b):
                p1 = FlexiblePlace(a)
                p2 = FlexiblePlace(b)
                lm = LocationMatrix([p1.get_location_components(), p2.get_location_components()])
                self.assertEqual(lm.row_count, 2)
                expected_cols = max(len(p1.get_location_components()), len(p2.get_location_components()))
                self.assertEqual(lm.column_count, expected_cols)
                # verify that each original non-empty component ended up somewhere in its row
                for idx, comp in enumerate(p1.get_location_components()):
                    self.assertEqual(lm.matrix[0][idx].value, comp)
                for idx, comp in enumerate(p2.get_location_components()):
                    self.assertEqual(lm.matrix[1][idx].value, comp)

    def test_groups_construct_ok(self):
        """Construct matrices for each group from combine tests and assert dimensions and presence of components"""
        for group in self.groups:
            with self.subTest(group=group):
                fps = [FlexiblePlace(s) for s in group]
                lm = LocationMatrix([fp.get_location_components() for fp in fps])
                self.assertEqual(lm.row_count, len(fps))
                expected_cols = max(len(fp.get_location_components()) for fp in fps) if fps else 0
                self.assertEqual(lm.column_count, expected_cols)
                # Check each provided non-empty component is present at the expected row/column
                for r, fp in enumerate(fps):
                    for c, comp in enumerate(fp.get_location_components()):
                        self.assertEqual(lm.matrix[r][c].value, comp)


if __name__ == "__main__":
    unittest.main()