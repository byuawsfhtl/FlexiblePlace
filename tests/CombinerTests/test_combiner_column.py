from FlexiblePlace.src.CombinerColumn import CombinerColumn


class TestCombinerColumn:
	"""Tests for the state and selection behavior of CombinerColumn."""

	def test_initializes_empty(self) -> None:
		"""A new column has no components, groups, or empty row indices."""
		column = CombinerColumn()

		assert column.components == []
		assert column.match_groups == []
		assert column.empty_indices == set()

	def test_add_component_preserves_order_and_tracks_empty_rows(self) -> None:
		"""Components retain row order and empty strings are recorded by row."""
		column = CombinerColumn()

		column.add_component("city")
		column.add_component("")
		column.add_component("state")
		column.add_component("")

		assert column.components == ["city", "", "state", ""]
		assert column.empty_indices == {1, 3}

	def test_add_match_group_ignores_empty_and_duplicate_groups(self) -> None:
		"""Only unique non-empty row groups are stored."""
		column = CombinerColumn()

		column.add_match_group(set())
		column.add_match_group({0, 1})
		column.add_match_group({1, 0})
		column.add_match_group({2})

		assert column.match_groups == [{0, 1}, {2}]

	def test_column_consensus_requires_one_group(self) -> None:
		"""No consensus exists when there are no groups or multiple groups."""
		column = CombinerColumn()
		column.components = ["Washington", "Washington"]

		assert column.column_consensus() == ""

		column.add_match_group({0})
		column.add_match_group({1})

		assert column.column_consensus() == ""

	def test_column_consensus_chooses_longest_component(self) -> None:
		"""The unique group consensus is its longest component."""
		column = CombinerColumn()
		column.components = ["WA", "Washington", "Washington state"]
		column.add_match_group({0, 1, 2})

		assert column.column_consensus() == "Washington state"

	def test_column_consensus_tie_uses_first_component(self) -> None:
		"""Equal-length components use the first row in the group."""
		column = CombinerColumn()
		column.components = ["Ohio", "Ohio"]
		column.add_match_group({0, 1})

		assert column.column_consensus() == "Ohio"

	def test_remove_match_group_updates_all_groups_and_empty_rows(self) -> None:
		"""Removing rows updates every group and removes emptied groups."""
		column = CombinerColumn()
		column.components = ["city", "city center", "country", "country region", ""]
		column.empty_indices = {4}
		column.match_groups = [{0, 1}, {2, 3}]

		column.remove_match_group({1, 3, 4})

		assert column.match_groups == [{0}, {2}]
		assert column.empty_indices == set()

	def test_remove_multiple_rows_from_one_group_removes_group_once(self) -> None:
		"""Removing all rows in one group is safe when multiple rows are passed."""
		column = CombinerColumn()
		column.components = ["city", "city center"]
		column.match_groups = [{0, 1}]

		column.remove_match_group({0, 1})

		assert column.match_groups == []

	def test_smallest_component_returns_shortest_row(self) -> None:
		"""The shortest grouped component identifies the row to remove."""
		column = CombinerColumn()
		column.components = ["city name", "city", "city region"]
		column.add_match_group({0, 1, 2})

		assert column.smallest_component() == 1

	def test_smallest_component_returns_none_when_lengths_are_equal(self) -> None:
		"""No row is selected when all grouped components have equal lengths."""
		column = CombinerColumn()
		column.components = ["Ohio", "Ohio"]
		column.add_match_group({0, 1})

		assert column.smallest_component() is None

	def test_smallest_component_returns_none_without_match_groups(self) -> None:
		"""An empty set of groups has no smallest component."""
		column = CombinerColumn()

		assert column.smallest_component() is None
		assert column._all_equal_length()

	def test_all_equal_length_detects_unequal_components(self) -> None:
		"""The helper detects a length difference across any grouped rows."""
		column = CombinerColumn()
		column.components = ["Ohio", "Ohio city", "Utah"]
		column.match_groups = [{0, 1}, {2}]

		assert not column._all_equal_length()

	def test_get_possible_rows_combines_grouped_and_empty_rows(self) -> None:
		"""Possible rows include all grouped rows followed by empty-component rows."""
		column = CombinerColumn()
		column.match_groups = [{2, 0}, {3}]
		column.empty_indices = {1}

		assert set(column.get_possible_rows()) == {0, 1, 2, 3}
