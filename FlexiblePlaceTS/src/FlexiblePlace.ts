import { autoFillLocation } from "./autoFillLocation";
import { Combiner } from "./combiner";
import { Compare } from "./compare";
import { getPlaceDescription } from "./getPlaceDescription";
import memoize from "memoizee";

/**
 * Represents a geographic location as normalized hierarchical components.
 *
 * Location components are stored in order from most specific to least specific,
 * normalized to lowercase, and can be compared or combined with other places.
 */
export class FlexiblePlace {
	location: Array<string>;
	placeDescription: string;

	/**
	 * Creates a place from a comma-separated string or component list.
	 *
	 * @param location - The location string or its components.
	 * @param placeDescription - FamilySearch place-description identifier.
	 * @param autoFill - Whether to infer "United States" for a trailing US state.
	 */
	constructor(
		location: string | Array<string>,
		placeDescription = "",
		autoFill = true
	) {
		const components = typeof location === "string" ? location.split(",") : location;
		this.location = components.map(component => component.trim().toLowerCase());
		if (autoFill) {
			autoFillLocation(this.location);
		}
		this.placeDescription = placeDescription;
	}

	/**
	 * Returns the place components in title case, joined with commas.
	 *
	 * @returns A human-readable location string.
	 */
	toString(): string {
		return this.getLocation()
			.map(component =>
				component.toLowerCase().replace(/(^|[^\p{L}\p{N}])(\p{L})/gu, (_match, prefix: string, letter: string) =>
					prefix + letter.toLocaleUpperCase()
				)
			)
			.join(", ");
	}

	/**
	 * Returns the FamilySearch place-description identifier.
	 *
	 * @returns The place-description identifier.
	 */
	toRepr(): string {
		return this.placeDescription;
	}

	/**
	 * Compares places by their normalized location components.
	 *
	 * @param other - The value to compare with this place.
	 * @returns True when the other value is a place with identical components.
	 */
	equals(other: unknown): boolean {
		return other instanceof FlexiblePlace &&
			this.location.length === other.location.length &&
			this.location.every((component, index) => component === other.location[index]);
	}

	/**
	 * Checks whether this place contains location components.
	 *
	 * @returns True when the location list is non-empty.
	 */
	booleanCheck(): boolean {
		return this.location.length > 0;
	}

	/**
	 * Returns this place's location components.
	 *
	 * @returns Components ordered from most specific to least specific.
	 */
	getLocation(): Array<string> {
		return this.location;
	}

	/**
	 * Compares this place with another place.
	 *
	 * @param other - The place to compare against.
	 * @returns A similarity score from 0 to 100.
	 */
	compare(other: FlexiblePlace): number {
		return FlexiblePlace.comparePlaces(this, other);
	}

	/**
	 * Compares two places by aligning and scoring their corresponding components.
	 *
	 * Empty places compare as a perfect match. Less-specific components have a
	 * greater influence on the resulting average than more-specific components.
	 *
	 * @param placeA - The first place.
	 * @param placeB - The second place.
	 * @returns A similarity score from 0 to 100.
	 */
	static comparePlaces(placeA: FlexiblePlace, placeB: FlexiblePlace): number {
		return FlexiblePlace._comparePlaces(placeA, placeB);
	}

	private static _comparePlaces = memoize(
		(placeA: FlexiblePlace, placeB: FlexiblePlace): number => {
			if (!placeA.booleanCheck() || !placeB.booleanCheck()) {
				return 100.0;
			}
			const alignedPlaces = Compare.alignComponents(placeA.location, placeB.location);
			const scores = Compare.compareEachComponent(alignedPlaces);
			Compare.adjustScores(scores);
			return Compare.getAverage(scores);
		},
		{ max: 1000 }
	);

	/**
	 * Combines multiple places and carries over the closest matching place description.
	 *
	 * @param places - Places to combine.
	 * @returns A new place representing the combined locations.
	 */
	static combineFlexiblePlaces(places: Array<FlexiblePlace>): FlexiblePlace {
		const combinedPlace = FlexiblePlace.generateCombinedPlace(places);
		const closestMatch = FlexiblePlace.findClosestMatch(combinedPlace, places);
		return new FlexiblePlace(combinedPlace, closestMatch.placeDescription);
	}

	/**
	 * Resolves conflicts and fills gaps across aligned place definitions.
	 *
	 * Rows are considered in this order: remove outliers, discard less-precise
	 * rows, discard rows with shorter components, then discard the last row.
	 * Column consensus fills the result where a unique matching group remains.
	 *
	 * @param places - Places to combine.
	 * @returns The combined location components.
	 */
	private static generateCombinedPlace(places: Array<FlexiblePlace>): Array<string> {
		const combiner = new Combiner(places.map(place => place.getLocation()));
		const combinedPlace = Array.from({ length: combiner.getColumnCount() }, () => "");
		const strategies = [
			() => combiner.removeOutliers(),
			() => combiner.removeLeastPrecise(),
			() => combiner.removeSmallestComponent(),
			() => combiner.removeLast()
		];

		while (Combiner.isNotFilled(combinedPlace)) {
			for (const strategy of strategies) {
				const startingRowCount = combiner.getRowCount();
				strategy();
				const hasChanged = combiner.fillIn(combinedPlace);
				if (hasChanged || startingRowCount > combiner.getRowCount()) {
					break;
				}
			}
			if (combiner.isEmpty()) {
				Combiner.resize(combinedPlace);
			}
		}
		return combinedPlace;
	}

	/**
	 * Finds the best described input place matching the combined location.
	 *
	 * Candidates must score at least 90; ties favor the place with more
	 * components. If there is no eligible candidate, the undescribed target is
	 * returned.
	 *
	 * @param combinedPlace - The combined location components.
	 * @param places - Input places to compare.
	 * @returns The closest match, or a new target place when none qualifies.
	 */
	private static findClosestMatch(
		combinedPlace: Array<string>,
		places: Array<FlexiblePlace>
	): FlexiblePlace {
		const target = new FlexiblePlace(combinedPlace, "", false);
		const scores = places.map(place => target.compare(place));
		let maxScore = Math.max(0, ...scores);
		if (maxScore < 90) {
			maxScore = 101;
		}
		const bestMatches = places.filter(
			(place, index) => scores[index] === maxScore && Boolean(place.placeDescription)
		);
		if (bestMatches.length === 0) {
			return target;
		}
		let bestMatch = bestMatches[0];
		for (const place of bestMatches.slice(1)) {
			if (place.location.length > bestMatch.location.length) {
				bestMatch = place;
			}
		}
		return bestMatch;
	}

	/**
	 * Combines places and retrieves a place description online when needed.
	 *
	 * @param places - Places to combine.
	 * @returns A new combined place with the best available place description.
	 */
	static async combineFlexiblePlacesOnline(
		places: Array<FlexiblePlace>
	): Promise<FlexiblePlace> {
		const combinedPlace = FlexiblePlace.generateCombinedPlace(places);
		const closestMatch = FlexiblePlace.findClosestMatch(combinedPlace, places);
		const temp = new FlexiblePlace(combinedPlace);
		const placeDescription =
			!closestMatch.placeDescription || closestMatch.location.length < temp.location.length
				? await getPlaceDescription(temp.toString())
				: closestMatch.placeDescription;
		return new FlexiblePlace(combinedPlace, placeDescription);
	}

	/**
	 * Creates a place and retrieves its FamilySearch place description if needed.
	 *
	 * @param location - The location string or its components.
	 * @param description - An existing place-description identifier, if available.
	 * @param autoFill - Whether to infer "United States" for a trailing US state.
	 * @returns The created place.
	 */
	static async online(
		location: string | Array<string>,
		description = "",
		autoFill = true
	): Promise<FlexiblePlace> {
		const temp = new FlexiblePlace(location, "", autoFill);
		const placeDescription = description || await getPlaceDescription(temp.toString());
		return new FlexiblePlace(temp.toString(), placeDescription, autoFill);
	}
}