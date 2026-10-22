/**
 * Stores components and related-row match groups for one aligned location column.
 */
export class CombinerColumn {
	components: Array<string> = [];
	matchGroups: Array<Set<number>> = [];
	emptyIndices: Set<number> = new Set();

	/** Adds a component and records its row when it is empty. */
	addComponent(component: string): void {
		if (!component) {
			this.emptyIndices.add(this.components.length);
		}
		this.components.push(component);
	}

	/**
	 * Adds a unique, non-empty group of related row indices.
	 *
	 * @param matchGroup - Row indices represented by this group.
	 */
	addMatchGroup(matchGroup: Set<number>): void {
		if (
			matchGroup.size > 0 &&
			!this.matchGroups.some(group =>
				group.size === matchGroup.size && [...group].every(row => matchGroup.has(row))
			)
		) {
			this.matchGroups.push(matchGroup);
		}
	}

	/** Removes row references from match groups and empty-row indices. */
	removeMatchGroup(rowsToRemove: Set<number>): void {
		for (const row of rowsToRemove) {
			this.emptyIndices.delete(row);
		}
		for (const group of this.matchGroups) {
			for (const row of rowsToRemove) {
				group.delete(row);
			}
		}
		this.matchGroups = this.matchGroups.filter(group => group.size > 0);
	}

	/**
	 * Returns the longest component when exactly one match group remains.
	 *
	 * @returns The group consensus, or an empty string when it is ambiguous.
	 */
	columnConsensus(): string {
		if (this.matchGroups.length !== 1) {
			return "";
		}
		let longest = "";
		for (const index of this.matchGroups[0]) {
			const component = this.components[index];
			if (component.length > longest.length) {
				longest = component;
			}
		}
		return longest;
	}

	/**
	 * Finds the row with the shortest component among the match groups.
	 *
	 * @returns The row index, or null when all grouped components have equal lengths.
	 */
	smallestComponent(): number | null {
		if (this.allEqualLength()) {
			return null;
		}
		let smallest = "";
		let smallestIndex: number | null = null;
		for (const group of this.matchGroups) {
			for (const index of group) {
				const component = this.components[index];
				if (!smallest || component.length < smallest.length) {
					smallest = component;
					smallestIndex = index;
				}
			}
		}
		return smallestIndex;
	}

	/** @returns True when all components in all match groups have equal lengths. */
	allEqualLength(): boolean {
		let first: string | undefined;
		for (const group of this.matchGroups) {
			for (const index of group) {
				const component = this.components[index];
				if (first === undefined) {
					first = component;
				} else if (first.length !== component.length) {
					return false;
				}
			}
		}
		return true;
	}

	/**
	 * Returns rows represented by match groups or empty components.
	 *
	 * @returns The possible row indices.
	 */
	getPossibleRows(): Array<number> {
		const rows: Array<number> = [];
		for (const group of this.matchGroups) {
			rows.push(...group);
		}
		rows.push(...this.emptyIndices);
		return rows;
	}
}
