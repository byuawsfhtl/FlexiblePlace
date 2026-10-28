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

if (require.main === module) {
	bridge.runCli(process.argv.slice(2));
}
