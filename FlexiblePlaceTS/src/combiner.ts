import { Aligner } from "./aligner";
import { CombinerColumn } from "./combinerColumn";

/**
 * Combines aligned location components into a complete location.
 *
 * Rows are stored as match groups per component column so outliers and
 * lower-confidence rows can be removed while constructing a consensus.
 */
export class Combiner {
	columns: Array<CombinerColumn>;

	/**
	 * Aligns the supplied locations and builds a column for each aligned component.
	 *
	 * @param locations - Location component lists, most specific to least specific.
	 */
	constructor(locations: Array<Array<string>>) {
		const aligner = new Aligner(locations);
		const alignedLocations = aligner.getLocations();
		const componentMatches = aligner.getLinks();
		this.columns = Array.from(
			{ length: aligner.columnCount },
			() => new CombinerColumn()
		);
		this.loadColumns(alignedLocations, componentMatches);
	}

	/**
	 * Loads aligned components and their match groups into the columns.
	 *
	 * @param alignedLocations - The aligned component rows.
	 * @param componentMatches - Row indices linked within each component column.
	 */
	private loadColumns(
		alignedLocations: Array<Array<string>>,
		componentMatches: Array<Array<Set<number>>>
	): void {
		for (let row = 0; row < alignedLocations.length; row++) {
			for (let column = 0; column < this.columns.length; column++) {
				this.columns[column].addComponent(alignedLocations[row][column]);
				this.columns[column].addMatchGroup(componentMatches[row][column]);
			}
		}
	}

	/** @returns The number of component columns. */
	getColumnCount(): number {
		return this.columns.length;
	}

	/** @returns The number of remaining rows represented by the first column. */
	getRowCount(): number {
		const firstColumn = this.columns[0];
		if (!firstColumn) {
			return 0;
		}
		return firstColumn.emptyIndices.size +
			firstColumn.matchGroups.reduce((count, group) => count + group.size, 0);
	}

	/** Removes rows in smaller match groups than the largest group in each column. */
	removeOutliers(): void {
		for (const column of [...this.columns].reverse()) {
			const largestGroup = Math.max(0, ...column.matchGroups.map(group => group.size));
			for (const group of [...column.matchGroups]) {
				if (group.size < largestGroup) {
					this.removeRows(new Set(group));
				}
			}
		}
	}

	/** Removes the given rows from every component column. */
	private removeRows(rows: Set<number>): void {
		for (const column of this.columns) {
			column.removeMatchGroup(rows);
		}
	}

	/**
	 * Removes the highest-indexed partial row from the least precise column.
	 *
	 * A partial row has an empty component in that column.
	 */
	removeLeastPrecise(): void {
		for (const column of [...this.columns].reverse()) {
			if (column.matchGroups.length > 0 && column.emptyIndices.size > 0) {
				const row = Math.max(...column.emptyIndices);
				this.removeRows(new Set([row]));
				return;
			}
		}
	}

	/** Removes the row containing the shortest component, if one can be selected. */
	removeSmallestComponent(): void {
		for (const column of [...this.columns].reverse()) {
			const row = column.smallestComponent();
			if (row !== null) {
				this.removeRows(new Set([row]));
				return;
			}
		}
	}

	/** Removes the highest-indexed remaining row. */
	removeLast(): void {
		if (this.isEmpty()) {
			return;
		}
		const possibleRows = this.columns[0].getPossibleRows();
		if (possibleRows.length > 0) {
			this.removeRows(new Set([Math.max(...possibleRows)]));
		}
	}

	/** @returns True when no possible rows remain. */
	isEmpty(): boolean {
		const firstColumn = this.columns[0];
		return !firstColumn ||
			(firstColumn.matchGroups.length === 0 && firstColumn.emptyIndices.size === 0);
	}

	/**
	 * Fills empty result components from columns with a unique match-group consensus.
	 *
	 * @param combinedPlace - The component list to update in place.
	 * @returns True when at least one component was filled.
	 */
	fillIn(combinedPlace: Array<string>): boolean {
		let changed = false;
		for (const [index, column] of this.columns.entries()) {
			const consensus = column.columnConsensus();
			if (consensus && !combinedPlace[index]) {
				combinedPlace[index] = consensus;
				changed = true;
			}
		}
		return changed;
	}

	/** @returns True when the combined location still has an empty component. */
	static isNotFilled(combinedLocation: Array<string>): boolean {
		return combinedLocation.includes("");
	}

	/** Removes empty components from the location in place. */
	static resize(combinedLocation: Array<string>): void {
		for (let index = combinedLocation.length - 1; index >= 0; index--) {
			if (!combinedLocation[index]) {
				combinedLocation.splice(index, 1);
			}
		}
	}
}
