use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Location {
    pub r#type: String,
    pub coordinates: Vec<f64>, // [longitude, latitude]
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct PlaceData {
    pub place: String,
    pub location: Option<Location>,
    pub placeid: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ScoreResult {
    pub physical_distance_score: f64,
    pub administrative_distance_score: f64,
    pub fuzzy_string_score: f64,
    pub master_score: f64,
    pub is_match: bool,
}

impl Default for ScoreResult {
    fn default() -> Self {
        Self {
            physical_distance_score: -1.0,
            administrative_distance_score: -1.0,
            fuzzy_string_score: -1.0,
            master_score: -1.0,
            is_match: false,
        }
    }
}
