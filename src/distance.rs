use haversine::{self, Location};
use crate::models::{Location as ModelLocation};

/// Calculates the physical distance score between two locations.
/// Higher score means closer proximity.
pub fn calculate_physical_score(loc_a: &ModelLocation, loc_b: &ModelLocation) -> f64 {
    if loc_a.coordinates.len() < 2 || loc_b.coordinates.len() < 2 {
        return -1.0;
    }

    let a = Location {
        latitude: loc_a.coordinates[1],
        longitude: loc_a.coordinates[0],
    };
    let b = Location {
        latitude: loc_b.coordinates[1],
        longitude: loc_b.coordinates[0],
    };

    let dist_km = haversine::distance(a, b, haversine::Units::Kilometers);

    // Turn distance (km) into a score.
    // 0 km -> 100 score.
    // > 1000 km -> 0 score.
    // A simple linear decay: 100 - (dist_km / 10).
    let score = 100.0 - (dist_km / 10.0);
    
    if score < 0.0 {
        0.0
    } else {
        score
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_physical_score_same() {
        let loc = ModelLocation {
            r#type: "Point".to_string(),
            coordinates: vec![2.0, 43.0],
        };
        let score = calculate_physical_score(&loc, &loc);
        assert_eq!(score, 100.0);
    }

    #[test]
    fn test_physical_score_close() {
        let loc_a = ModelLocation {
            r#type: "Point".to_string(),
            coordinates: vec![2.0, 43.0],
        };
        let loc_b = ModelLocation {
            r#type: "Point".to_string(),
            coordinates: vec![2.1, 43.1],
        };
        let score = calculate_physical_score(&loc_a, &loc_b);
        assert!(score > 90.0 && score < 100.0);
    }
}
