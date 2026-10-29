import { FlexiblePlace } from "./src/FlexiblePlace";
import { Aligner } from "./src/aligner";
import { autoFillLocation } from "./src/autoFillLocation";
import { Combiner } from "./src/combiner";
import { CombinerColumn } from "./src/combinerColumn";
import { Compare } from "./src/compare";
import { basicComparisonAlgorithm } from "./src/compareLocationComponents";
import { getPlaceDescription } from "./src/getPlaceDescription";
import { LocationComponent } from "./src/locationComponent";
import { PyScriptTestBridge } from 'pyscripttestutils';

function serializeFlexiblePlace(value: any): any {
	if (value instanceof FlexiblePlace) {
		return {
			__type: "FlexiblePlace",
			location: value.getLocation(),
			placeDescription: value.placeDescription
		};
	}
	if (value instanceof LocationComponent) {
		return {
			__type: "LocationComponent",
			pair: value.pair,
			value: value.value
		};
	}
	if (value instanceof Aligner) {
		return {
			__type: "Aligner",
			locations: value.getLocations()
		};
	}
	if (value instanceof Combiner) {
		return { __type: "Combiner", columns: value.columns };
	}
	if (value instanceof CombinerColumn) {
		return {
			__type: "CombinerColumn",
			components: value.components,
			matchGroups: [...value.matchGroups].map(group => [...group]),
			emptyIndices: [...value.emptyIndices]
		};
	}
	if (value instanceof Set) {
		return [...value];
	}
	if (Array.isArray(value)) {
		return value.map(item => serializeFlexiblePlace(item));
	}
	return value;
}

function deserializeFlexiblePlace(data: any): any {
	if (data === null || typeof data !== "object") {
		return data;
	}
	if (Array.isArray(data)) {
		return data.map(item => deserializeFlexiblePlace(item));
	}

	if (data.__type === "FlexiblePlace" || "location" in data) {
		return new FlexiblePlace(
			data.location,
			data.placeDescription ?? "",
			false
		);
	}
	if (data.__type === "LocationComponent") {
		return new LocationComponent(data.pair, data.value ?? "");
	}
	if (data.__type === "Aligner") {
		return new Aligner(data.locations);
	}
	if (data.__type === "CombinerColumn") {
		const column = new CombinerColumn();
		for (const component of data.components ?? []) {
			column.addComponent(component);
		}
		for (const group of data.matchGroups ?? []) {
			column.addMatchGroup(new Set(group));
		}
		column.emptyIndices = new Set(data.emptyIndices ?? []);
		return column;
	}
	if (data.__type === "Combiner") {
		const combiner = Object.create(Combiner.prototype) as Combiner;
		combiner.columns = (data.columns ?? []).map((column: any) => deserializeFlexiblePlace({ __type: "CombinerColumn", ...column }));
		return combiner;
	}
	return data;
}

const bridge = new PyScriptTestBridge(serializeFlexiblePlace, deserializeFlexiblePlace);

bridge.addMethod("createFlexiblePlace", (args) => {
	return new FlexiblePlace(args[0], args[1] ?? "", args[2] ?? true);
});

bridge.addMethod("FlexiblePlace.online", async (args) => {
	return await FlexiblePlace.online(args[0], args[1] ?? "", args[2] ?? true);
});

bridge.addMethod("FlexiblePlace.getLocation", (args) => args[0].getLocation());
bridge.addMethod("FlexiblePlace.get_location", (args) => args[0].getLocation());

bridge.addMethod("FlexiblePlace.compare", (args) => args[0].compare(args[1]));
bridge.addMethod("comparePlaces", (args) => FlexiblePlace.comparePlaces(args[0], args[1]));
bridge.addMethod("FlexiblePlace.comparePlaces", (args) => FlexiblePlace.comparePlaces(args[0], args[1]));
bridge.addMethod("FlexiblePlace.compare_places", (args) => FlexiblePlace.comparePlaces(args[0], args[1]));

bridge.addMethod("combineFlexiblePlaces", (args) => {
	return FlexiblePlace.combineFlexiblePlaces(args[0]);
});
bridge.addMethod("FlexiblePlace.combineFlexiblePlaces", (args) => {
	return FlexiblePlace.combineFlexiblePlaces(args[0]);
});
bridge.addMethod("FlexiblePlace.combine_flexible_places", (args) => {
	return FlexiblePlace.combineFlexiblePlaces(args[0]);
});

bridge.addMethod("FlexiblePlace.combineFlexiblePlacesOnline", async (args) => {
	return await FlexiblePlace.combineFlexiblePlacesOnline(args[0]);
});
bridge.addMethod("FlexiblePlace.combine_flexible_places_online", async (args) => {
	return await FlexiblePlace.combineFlexiblePlacesOnline(args[0]);
});

bridge.addMethod("FlexiblePlace.toString", (args) => args[0].toString());
bridge.addMethod("FlexiblePlace.__str__", (args) => args[0].toString());
bridge.addMethod("FlexiblePlace.toRepr", (args) => args[0].toRepr());
bridge.addMethod("FlexiblePlace.__repr__", (args) => args[0].toRepr());
bridge.addMethod("FlexiblePlace.valueOf", (args) => args[0].booleanCheck());
bridge.addMethod("FlexiblePlace.__bool__", (args) => args[0].booleanCheck());
bridge.addMethod("FlexiblePlace.equals", (args) => args[0].equals(args[1]));
bridge.addMethod("FlexiblePlace.__eq__", (args) => args[0].equals(args[1]));
bridge.addMethod("FlexiblePlace.hash", (args) => JSON.stringify(args[0].getLocation()));

bridge.addMethod("autoFillLocation", (args) => {
	const location = [...args[0]];
	autoFillLocation(location);
	return location;
});
bridge.addMethod("auto_fill_location", (args) => {
	const location = [...args[0]];
	autoFillLocation(location);
	return location;
});

bridge.addMethod("getPlaceDescription", async (args) => getPlaceDescription(args[0]));
bridge.addMethod("get_place_description", async (args) => getPlaceDescription(args[0]));
bridge.addMethod("basicComparisonAlgorithm", (args) => basicComparisonAlgorithm(args[0], args[1]));
bridge.addMethod("basic_comparison_algorithm", (args) => basicComparisonAlgorithm(args[0], args[1]));

bridge.addMethod("Compare.alignComponents", (args) => Compare.alignComponents(args[0], args[1]));
bridge.addMethod("Compare.align_components", (args) => Compare.alignComponents(args[0], args[1]));
bridge.addMethod("Compare.compareEachComponent", (args) => Compare.compareEachComponent(args[0]));
bridge.addMethod("Compare.compare_each_component", (args) => Compare.compareEachComponent(args[0]));
bridge.addMethod("Compare.adjustScores", (args) => {
	Compare.adjustScores(args[0]);
	return args[0];
});
bridge.addMethod("Compare.adjust_scores", (args) => {
	Compare.adjustScores(args[0]);
	return args[0];
});
bridge.addMethod("Compare.getAverage", (args) => Compare.getAverage(args[0]));
bridge.addMethod("Compare.get_average", (args) => Compare.getAverage(args[0]));

bridge.addMethod("createAligner", (args) => new Aligner(args[0]));
bridge.addMethod("Aligner.valueOf", (args) => args[0].toBoolean());
bridge.addMethod("Aligner.toBoolean", (args) => args[0].toBoolean());
bridge.addMethod("Aligner.__bool__", (args) => args[0].toBoolean());
bridge.addMethod("Aligner.toString", (args) => args[0].toString());
bridge.addMethod("Aligner.__str__", (args) => args[0].toString());
bridge.addMethod("Aligner.get", (args) => args[0].get(args[1], args[2]));
bridge.addMethod("Aligner.getLocations", (args) => args[0].getLocations());
bridge.addMethod("Aligner.get_locations", (args) => args[0].getLocations());
bridge.addMethod("Aligner.getRow", (args) => args[0].getRow(args[1]));
bridge.addMethod("Aligner.get_row", (args) => args[0].getRow(args[1]));
bridge.addMethod("Aligner.getColumn", (args) => args[0].getColumn(args[1]));
bridge.addMethod("Aligner.get_column", (args) => args[0].getColumn(args[1]));
bridge.addMethod("Aligner.insert", (args) => args[0].insert(args[1]));
bridge.addMethod("Aligner.loadPlaces", (args) => args[0].loadPlaces(args[1]));
bridge.addMethod("Aligner.load_places", (args) => args[0].loadPlaces(args[1]));
bridge.addMethod("Aligner.align", (args) => args[0].align());
bridge.addMethod("Aligner.link", (args) => args[0].link(args[1], args[2]));
bridge.addMethod("Aligner.getLinks", (args) => args[0].getLinks());
bridge.addMethod("Aligner.get_links", (args) => args[0].getLinks());

bridge.addMethod("createLocationComponent", (args) => new LocationComponent(args[0], args[1] ?? ""));
bridge.addMethod("LocationComponent.valueOf", (args) => args[0].booleanCheck());
bridge.addMethod("LocationComponent.toBoolean", (args) => args[0].booleanCheck());
bridge.addMethod("LocationComponent.__bool__", (args) => args[0].booleanCheck());
bridge.addMethod("LocationComponent.toString", (args) => args[0].toString());
bridge.addMethod("LocationComponent.__str__", (args) => args[0].toString());
bridge.addMethod("LocationComponent.equals", (args) => args[0].equals(args[1]));
bridge.addMethod("LocationComponent.__eq__", (args) => args[0].equals(args[1]));
bridge.addMethod("LocationComponent.link", (args) => args[0].link(args[1]));

bridge.addMethod("createCombiner", (args) => new Combiner(args[0]));
bridge.addMethod("Combiner.getColumnCount", (args) => args[0].getColumnCount());
bridge.addMethod("Combiner.get_column_count", (args) => args[0].getColumnCount());
bridge.addMethod("Combiner.getRowCount", (args) => args[0].getRowCount());
bridge.addMethod("Combiner.get_row_count", (args) => args[0].getRowCount());
bridge.addMethod("Combiner.removeOutliers", (args) => args[0].removeOutliers());
bridge.addMethod("Combiner.remove_outliers", (args) => args[0].removeOutliers());
bridge.addMethod("Combiner.removeLeastPrecise", (args) => args[0].removeLeastPrecise());
bridge.addMethod("Combiner.remove_least_precise", (args) => args[0].removeLeastPrecise());
bridge.addMethod("Combiner.removeSmallestComponent", (args) => args[0].removeSmallestComponent());
bridge.addMethod("Combiner.remove_smallest_component", (args) => args[0].removeSmallestComponent());
bridge.addMethod("Combiner.removeLast", (args) => args[0].removeLast());
bridge.addMethod("Combiner.remove_last", (args) => args[0].removeLast());
bridge.addMethod("Combiner.isEmpty", (args) => args[0].isEmpty());
bridge.addMethod("Combiner.is_empty", (args) => args[0].isEmpty());
bridge.addMethod("Combiner.fillIn", (args) => args[0].fillIn(args[1]));
bridge.addMethod("Combiner.fill_in", (args) => args[0].fillIn(args[1]));
bridge.addMethod("Combiner.isNotFilled", (args) => Combiner.isNotFilled(args[0]));
bridge.addMethod("Combiner.is_not_filled", (args) => Combiner.isNotFilled(args[0]));
bridge.addMethod("Combiner.resize", (args) => Combiner.resize(args[0]));

bridge.addMethod("createCombinerColumn", () => new CombinerColumn());
bridge.addMethod("CombinerColumn.addComponent", (args) => args[0].addComponent(args[1]));
bridge.addMethod("CombinerColumn.add_component", (args) => args[0].addComponent(args[1]));
bridge.addMethod("CombinerColumn.addMatchGroup", (args) => args[0].addMatchGroup(new Set(args[1])));
bridge.addMethod("CombinerColumn.add_match_group", (args) => args[0].addMatchGroup(new Set(args[1])));
bridge.addMethod("CombinerColumn.removeMatchGroup", (args) => args[0].removeMatchGroup(new Set(args[1])));
bridge.addMethod("CombinerColumn.remove_match_group", (args) => args[0].removeMatchGroup(new Set(args[1])));
bridge.addMethod("CombinerColumn.columnConsensus", (args) => args[0].columnConsensus());
bridge.addMethod("CombinerColumn.column_consensus", (args) => args[0].columnConsensus());
bridge.addMethod("CombinerColumn.smallestComponent", (args) => args[0].smallestComponent());
bridge.addMethod("CombinerColumn.smallest_component", (args) => args[0].smallestComponent());
bridge.addMethod("CombinerColumn.allEqualLength", (args) => args[0].allEqualLength());
bridge.addMethod("CombinerColumn._all_equal_length", (args) => args[0].allEqualLength());
bridge.addMethod("CombinerColumn.getPossibleRows", (args) => args[0].getPossibleRows());
bridge.addMethod("CombinerColumn.get_possible_rows", (args) => args[0].getPossibleRows());

if (require.main === module) {
	bridge.runCli(process.argv.slice(2));
}
