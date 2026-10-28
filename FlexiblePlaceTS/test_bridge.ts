import { FlexiblePlace } from "./src/FlexiblePlace";
import { PyScriptTestBridge } from 'pyscripttestutils';

function serializeFlexiblePlace(flexiblePlace: FlexiblePlace): any{
	if(flexiblePlace.constructor.name === "FlexiblePlace"){
		return {
			location: flexiblePlace.getLocation(),
			placeDescription: flexiblePlace.placeDescription
		}
	}
	return flexiblePlace;
}

function deserializeFlexiblePlace(data: any): FlexiblePlace{
	if("location" in data){
		if("placeDescription" in data){
			return new FlexiblePlace(data.location,data.placeDescription,false)
		}
		return new FlexiblePlace(data.location,"",false)
	}
	return data
}

const bridge = new PyScriptTestBridge(serializeFlexiblePlace, deserializeFlexiblePlace);
