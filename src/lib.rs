pub mod models;
pub mod fuzzy;
pub mod admin;
pub mod distance;
pub mod db;

use models::{PlaceData, ScoreResult};
use fuzzy::calculate_fuzzy_score;
use admin::calculate_admin_score;
use distance::calculate_physical_score;
use db::lookup_place;
use tokio::runtime::Runtime;

#[cfg(feature = "python")]
use pyo3::prelude::*;
#[cfg(feature = "python")]
use pyo3::types::PyDict;

#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;

lazy_static::lazy_static! {
    static ref RT: Runtime = Runtime::new().expect("Failed to create Tokio runtime");
}

/// Main function to calculate the similarity score using provided data.
pub fn compare_by_data(data1: &PlaceData, data2: &PlaceData) -> ScoreResult {
    let mut result = ScoreResult::default();

    // 1. Physical Distance Score
    if let (Some(loc1), Some(loc2)) = (&data1.location, &data2.location) {
        result.physical_distance_score = calculate_physical_score(loc1, loc2);
    }

    // 2. Administrative Distance Score
    result.administrative_distance_score = calculate_admin_score(&data1.place, &data2.place);

    // 3. Fuzzy String Score
    result.fuzzy_string_score = calculate_fuzzy_score(&data1.place, &data2.place);

    // 4. Master Score
    let mut scores = Vec::new();
    if result.physical_distance_score >= 0.0 {
        scores.push(result.physical_distance_score);
    }
    if result.administrative_distance_score >= 0.0 {
        scores.push(result.administrative_distance_score);
    }
    if result.fuzzy_string_score >= 0.0 {
        scores.push(result.fuzzy_string_score);
    }

    if !scores.is_empty() {
        result.master_score = scores.iter().sum::<f64>() / scores.len() as f64;
    }

    // Match flag
    let threshold = 80.0;
    result.is_match = result.master_score > threshold;

    result
}

// --- Common Logic for Python and WASM ---

fn compare_places_logic(name1: String, name2: String) -> Result<ScoreResult, String> {
    RT.block_on(async {
        let p1 = lookup_place(&name1).await?.unwrap_or(PlaceData {
            place: name1.clone(),
            location: None,
            placeid: None,
        });
        let p2 = lookup_place(&name2).await?.unwrap_or(PlaceData {
            place: name2.clone(),
            location: None,
            placeid: None,
        });

        Ok(compare_by_data(&p1, &p2))
    })
}

fn compare_places_from_json_logic(data1_json: &str, data2_json: &str) -> Result<ScoreResult, String> {
    let p1: PlaceData = serde_json::from_str(data1_json).map_err(|e| e.to_string())?;
    let p2: PlaceData = serde_json::from_str(data2_json).map_err(|e| e.to_string())?;
    Ok(compare_by_data(&p1, &p2))
}

// --- Python Bindings ---

#[cfg(feature = "python")]
#[pyfunction]
fn compare_places(name1: String, name2: String) -> PyResult<PyObject> {
    let result = compare_places_logic(name1, name2)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e))?;

    Python::with_gil(|py| {
        let dict = PyDict::new_bound(py);
        dict.set_item("physical_distance_score", result.physical_distance_score)?;
        dict.set_item("administrative_distance_score", result.administrative_distance_score)?;
        dict.set_item("fuzzy_string_score", result.fuzzy_string_score)?;
        dict.set_item("master_score", result.master_score)?;
        dict.set_item("is_match", result.is_match)?;
        Ok(dict.to_object(py))
    })
}

#[cfg(feature = "python")]
#[pyfunction]
fn compare_places_from_json(data1_json: String, data2_json: String) -> PyResult<PyObject> {
    let result = compare_places_from_json_logic(&data1_json, &data2_json)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e))?;

    Python::with_gil(|py| {
        let dict = PyDict::new_bound(py);
        dict.set_item("physical_distance_score", result.physical_distance_score)?;
        dict.set_item("administrative_distance_score", result.administrative_distance_score)?;
        dict.set_item("fuzzy_string_score", result.fuzzy_string_score)?;
        dict.set_item("master_score", result.master_score)?;
        dict.set_item("is_match", result.is_match)?;
        Ok(dict.to_object(py))
    })
}

#[cfg(feature = "python")]
#[pymodule]
fn placecomparator(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(compare_places, m)?)?;
    m.add_function(wrap_pyfunction!(compare_places_from_json, m)?)?;
    Ok(())
}

// --- WebAssembly Bindings ---

#[cfg(feature = "wasm")]
#[wasm_bindgen(js_name = comparePlaces)]
pub async fn compare_places_wasm(name1: String, name2: String) -> Result<JsValue, JsValue> {
    let result = RT.block_on(async {
        let p1 = lookup_place(&name1).await.map_err(|e| e.to_string())?.unwrap_or(PlaceData {
            place: name1.clone(),
            location: None,
            placeid: None,
        });
        let p2 = lookup_place(&name2).await.map_err(|e| e.to_string())?.unwrap_or(PlaceData {
            place: name2.clone(),
            location: None,
            placeid: None,
        });

        Ok::<ScoreResult, String>(compare_by_data(&p1, &p2))
    }).map_err(|e| JsValue::from_str(&e))?;
    
    serde_wasm_bindgen::to_value(&result).map_err(|e| JsValue::from_str(&e.to_string()))
}

#[cfg(feature = "wasm")]
#[wasm_bindgen(js_name = comparePlacesFromJson)]
pub fn compare_places_from_json_wasm(data1_json: &str, data2_json: &str) -> Result<JsValue, JsValue> {
    let result = compare_places_from_json_logic(data1_json, data2_json).map_err(|e| JsValue::from_str(&e))?;
    serde_wasm_bindgen::to_value(&result).map_err(|e| JsValue::from_str(&e.to_string()))
}
