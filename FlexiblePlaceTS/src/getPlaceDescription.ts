interface PlaceSearchResponse {
	entries?: Array<unknown>;
}

function isRecord(value: unknown): value is Record<string, unknown> {
	return typeof value === "object" && value !== null;
}

function isPlaceSearchResponse(value: unknown): value is PlaceSearchResponse {
	return isRecord(value) &&
		(value.entries === undefined || Array.isArray(value.entries));
}

/**
 * Queries FamilySearch for a high-confidence place description.
 *
 * @param location - The location string to search for.
 * @returns The matching place-description identifier, or an empty string when
 *          the location is blank, the response has no result, or the top score is below 95.
 * @throws If the request fails or the response cannot be parsed.
 */
export async function getPlaceDescription(location: string): Promise<string> {
	const trimmedLocation = location.trim();
	if (!trimmedLocation) {
		return "";
	}

	const query = new URLSearchParams({ q: `name:"${trimmedLocation}"` });
	const response = await fetch(
		`https://api.familysearch.org/platform/places/search?${query.toString()}`
	);
	if (response.status !== 200) {
		return "";
	}

	const data: unknown = await response.json();
	if (!isPlaceSearchResponse(data) || !Array.isArray(data.entries) || data.entries.length === 0) {
		return "";
	}

	const entry = data.entries[0];
	if (
		!isRecord(entry) ||
		typeof entry.score !== "number" ||
		entry.score < 95 ||
		typeof entry.id !== "string"
	) {
		return "";
	}
	return entry.id;
}
