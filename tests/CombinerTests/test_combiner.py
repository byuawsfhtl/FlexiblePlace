from FlexiblePlace.src.Combiner import Combiner
from FlexiblePlace.src.CombinerColumn import CombinerColumn


def make_combiner(columns: list[CombinerColumn]) -> Combiner:
	"""Create a Combiner with controlled columns for strategy-level tests."""
	combiner = object.__new__(Combiner)
	combiner.columns = columns
	return combiner


def make_column(
	components: list[str],
	match_groups: list[set[int]],
	empty_indices: set[int] | None = None,
) -> CombinerColumn:
	"""Create a CombinerColumn fixture without invoking alignment."""
	column = CombinerColumn()
	column.components = components
	column.match_groups = match_groups
	column.empty_indices = empty_indices or set()
	return column


class TestCombiner:
	"""Tests for Combiner coordination and location-combination helpers."""

	def test_initializes_columns_from_aligned_locations(self) -> None:
		"""Construction loads aligned components and their row links."""
		combiner = Combiner([
			["springfield", "illinois", "united states"],
			["springfield", "illinois"],
		])

		assert combiner.get_column_count() == 3
		assert combiner.get_row_count() == 2
		assert combiner.columns[0].components == ["springfield", "springfield"]

	def test_initializes_with_no_columns_for_empty_input(self) -> None:
		"""An empty location collection creates a valid zero-column combiner."""
		combiner = Combiner([])

		assert combiner.columns == []
		assert combiner.get_column_count() == 0

	def test_load_columns_populates_each_column(self) -> None:
		"""Aligned values and match groups are loaded row by row."""
		combiner = make_combiner([CombinerColumn(), CombinerColumn()])

		combiner._load_columns(
			[["springfield", "illinois"], ["springfield", "illinois"]],
			[[{0, 1}, {0, 1}], [{0, 1}, {0, 1}]],
		)

		assert combiner.columns[0].components == ["springfield", "springfield"]
		assert combiner.columns[1].components == ["illinois", "illinois"]
		assert combiner.columns[0].match_groups == [{0, 1}]
		assert combiner.columns[1].match_groups == [{0, 1}]

	def test_get_counts_include_only_current_rows(self) -> None:
		"""Column and row counts reflect the current combiner state."""
		city_components = ["city", "city center", ""]
		city_match_groups = [{0, 1}]
		city_empty_indices = {2}
		state_components = ["state", "state region", ""]
		state_match_groups = [{0, 1}]
		state_empty_indices = {2}
		combiner = make_combiner([
			make_column(city_components, city_match_groups, city_empty_indices),
			make_column(state_components, state_match_groups, state_empty_indices),
		])

		assert combiner.get_column_count() == 2
		assert combiner.get_row_count() == 3

		combiner._remove_rows({1})

		assert combiner.get_row_count() == 2

	def test_remove_outliers_removes_smaller_groups(self) -> None:
		"""Remove rows belonging to smaller match groups across every column.

		Before: city groups are ``{0, 1}`` and ``{2}``, and state groups are
		``{0, 1}`` and ``{2}``.
		After: row ``2`` is removed from both columns, leaving only rows ``0``
		and ``1``.
		"""
		city_components = ["springfield", "springfield city", "springfield village"]
		city_match_groups = [{0, 1}, {2}]
		city_empty_indices: set[int] = set()
		state_components = ["illinois", "illinois state", "illinois region"]
		state_match_groups = [{0, 1}, {2}]
		state_empty_indices: set[int] = set()
		combiner = make_combiner([
			make_column(city_components, city_match_groups, city_empty_indices),
			make_column(state_components, state_match_groups, state_empty_indices),
		])

		combiner.remove_outliers()

		assert combiner.get_row_count() == 2
		assert all(2 not in group for column in combiner.columns for group in column.match_groups)

	def test_remove_rows_updates_every_column(self) -> None:
		"""Remove the requested row from every column and row-tracking set.

		Before: both columns contain grouped rows ``{0, 1}`` and empty row ``2``.
		After: removing row ``1`` leaves group ``{0}``; no column still refers
		to row ``1``.
		"""
		city_components = ["city", "city center", ""]
		city_match_groups = [{0, 1}]
		city_empty_indices = {2}
		state_components = ["state", "state region", ""]
		state_match_groups = [{0, 1}]
		state_empty_indices = {2}
		combiner = make_combiner([
			make_column(city_components, city_match_groups, city_empty_indices),
			make_column(state_components, state_match_groups, state_empty_indices),
		])

		combiner._remove_rows({1})

		assert all(1 not in group for column in combiner.columns for group in column.match_groups)
		assert all(1 not in column.empty_indices for column in combiner.columns)

	def test_remove_least_precise_removes_highest_partial_row(self) -> None:
		"""Remove the highest-indexed row with a missing component.

		Before: the city column has empty rows ``{2, 3}``, while the state column
		has empty row ``{3}``.
		After: row ``3`` is removed from every column, leaving row ``2`` as the
		only partial row.
		"""
		city_components = ["city", "city center", "", ""]
		city_match_groups = [{0, 1}]
		city_empty_indices = {2, 3}
		state_components = ["state", "state region", "state county", ""]
		state_match_groups = [{0, 1, 2}]
		state_empty_indices = {3}
		combiner = make_combiner([
			make_column(city_components, city_match_groups, city_empty_indices),
			make_column(state_components, state_match_groups, state_empty_indices),
		])

		combiner.remove_least_precise()

		assert combiner.get_row_count() == 3
		assert all(3 not in group for column in combiner.columns for group in column.match_groups)
		assert all(3 not in column.empty_indices for column in combiner.columns)

	def test_remove_smallest_component_removes_shortest_grouped_row(self) -> None:
		"""Remove the row containing the shortest grouped component.

		Before: the state values are ``["illinois state", "illinois",
		"illinois county"]`` for rows ``0``, ``1``, and ``2``.
		After: row ``1`` is removed because ``"illinois"`` is the
		first component to be shorter than the rest in the column. This leaves
		rows ``0`` and ``2``.
		"""
		city_components = ["springfield city", "springfield", "springfield village"]
		city_match_groups = [{0, 1, 2}]
		city_empty_indices: set[int] = set()
		state_components = ["illinois state", "illinois", "illinois county"]
		state_match_groups = [{0, 1, 2}]
		state_empty_indices: set[int] = set()
		combiner = make_combiner([
			make_column(city_components, city_match_groups, city_empty_indices),
			make_column(state_components, state_match_groups, state_empty_indices),
		])

		combiner.remove_smallest_component()

		assert combiner.get_row_count() == 2
		assert all(1 not in group for column in combiner.columns for group in column.match_groups)

	def test_remove_last_removes_highest_possible_row(self) -> None:
		"""Remove the highest row still represented by the first column.

		Before: the first column represents rows ``0``, ``1``, and ``2``, with
		row ``2`` represented by an empty component.
		After: row ``2`` is removed from both columns, leaving rows ``0`` and
		``1`` available.
		"""
		city_components = ["city", "city center", ""]
		city_match_groups = [{0, 1}]
		city_empty_indices = {2}
		state_components = ["state", "state region", ""]
		state_match_groups = [{0, 1}]
		state_empty_indices = {2}
		combiner = make_combiner([
			make_column(city_components, city_match_groups, city_empty_indices),
			make_column(state_components, state_match_groups, state_empty_indices),
		])

		combiner.remove_last()

		assert combiner.is_empty() is False
		assert combiner.get_row_count() == 2
		assert all(2 not in group for column in combiner.columns for group in column.match_groups)
		assert all(2 not in column.empty_indices for column in combiner.columns)

	def test_remove_last_does_nothing_when_empty(self) -> None:
		"""Do nothing when there are no rows to delete.

		Before: the combiner has no groups and no empty row indices.
		After: the combiner remains empty and unchanged.
		"""
		combiner = make_combiner([CombinerColumn()])

		combiner.remove_last()

		assert combiner.is_empty()

	def test_is_empty_tracks_first_column_rows(self) -> None:
		"""The combiner becomes empty after all first-column rows are removed."""
		city_components = ["city"]
		city_match_groups = [{0}]
		city_empty_indices: set[int] = set()
		state_components = ["state"]
		state_match_groups = [{0}]
		state_empty_indices: set[int] = set()
		combiner = make_combiner([
			make_column(city_components, city_match_groups, city_empty_indices),
			make_column(state_components, state_match_groups, state_empty_indices),
		])

		assert not combiner.is_empty()
		combiner._remove_rows({0})
		assert combiner.is_empty()

	def test_fill_in_fills_only_empty_components_with_unique_consensus(self) -> None:
		"""Filling mutates empty slots but does not overwrite values or ambiguity."""
		city_components = ["springfield", "springfield city"]
		city_match_groups = [{0, 1}]
		city_empty_indices: set[int] = set()
		state_components = ["illinois", "illinois state", "indiana"]
		state_match_groups = [{0, 1}, {2}]
		state_empty_indices: set[int] = set()
		combiner = make_combiner([
			make_column(city_components, city_match_groups, city_empty_indices),
			make_column(state_components, state_match_groups, state_empty_indices),
		])
		combined_place = ["", "existing"]

		assert combiner.fill_in(combined_place)
		assert combined_place == ["springfield city", "existing"]

	def test_fill_in_returns_false_when_nothing_can_change(self) -> None:
		"""No consensus or already-filled positions produce no mutation."""
		city_components = ["springfield"]
		city_match_groups = [{0}]
		city_empty_indices: set[int] = set()
		state_components = ["illinois", "indiana"]
		state_match_groups = [{0}, {1}]
		state_empty_indices: set[int] = set()
		combiner = make_combiner([
			make_column(city_components, city_match_groups, city_empty_indices),
			make_column(state_components, state_match_groups, state_empty_indices),
		])
		combined_place = ["springfield", ""]

		assert not combiner.fill_in(combined_place)
		assert combined_place == ["springfield", ""]

	def test_static_fill_and_resize_helpers(self) -> None:
		"""Static helpers detect missing values and remove empty trailing slots."""
		location = ["springfield", "", "illinois", ""]

		assert Combiner.is_not_filled(location)
		Combiner.resize(location)
		assert location == ["springfield", "illinois"]
		assert not Combiner.is_not_filled(location)

	def test_static_helpers_handle_empty_locations(self) -> None:
		"""Empty lists are already filled and remain unchanged when resized."""
		location: list[str] = []

		assert not Combiner.is_not_filled(location)
		Combiner.resize(location)
		assert location == []


