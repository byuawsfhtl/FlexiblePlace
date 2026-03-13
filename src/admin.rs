/// Calculates the administrative distance between two places.
/// Formula: D_adm = wr * depth(lr) + wt * depth(lt) - (wr + wt) * depth(LCA(lr, lt))
pub fn calculate_admin_score(place_a: &str, place_b: &str) -> f64 {
    let parts_a: Vec<&str> = place_a.split(',').map(|s| s.trim()).filter(|s| !s.is_empty()).collect();
    let parts_b: Vec<&str> = place_b.split(',').map(|s| s.trim()).filter(|s| !s.is_empty()).collect();

    if parts_a.is_empty() || parts_b.is_empty() {
        return -1.0;
    }

    // Depth is the number of parts (reversed, assuming last part is country/root)
    let depth_a = parts_a.len();
    let depth_b = parts_b.len();

    // Find LCA (Lowest Common Ancestor)
    // Assuming parts are [City, County, Country]
    // LCA depth is the number of matching parts from the end
    let mut lca_depth = 0;
    let mut a_iter = parts_a.iter().rev();
    let mut b_iter = parts_b.iter().rev();

    while let (Some(a), Some(b)) = (a_iter.next(), b_iter.next()) {
        if a.eq_ignore_ascii_case(b) {
            lca_depth += 1;
        } else {
            break;
        }
    }

    // Weights (wr and wt) - uniform at country level for now
    let wr = 1.0;
    let wt = 1.0;

    let d_adm = wr * (depth_a as f64) + wt * (depth_b as f64) - (wr + wt) * (lca_depth as f64);

    // Turn distance into a score (e.g., higher score means more similar)
    // A simple way: 100 / (1 + d_adm)
    100.0 / (1.0 + d_adm)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_admin_score_same() {
        let score = calculate_admin_score("Villepinte, Aude, France", "Villepinte, Aude, France");
        assert_eq!(score, 100.0);
    }

    #[test]
    fn test_admin_score_same_county() {
        let score = calculate_admin_score("Villepinte, Aude, France", "Carcassonne, Aude, France");
        // depth_a = 3, depth_b = 3, lca_depth = 2 (Aude, France)
        // d_adm = 1*3 + 1*3 - (1+1)*2 = 6 - 4 = 2
        // score = 100 / (1 + 2) = 33.33
        assert!(score > 33.0 && score < 34.0);
    }

    #[test]
    fn test_admin_score_different_country() {
        let score = calculate_admin_score("Villepinte, Aude, France", "London, UK");
        // depth_a = 3, depth_b = 2, lca_depth = 0
        // d_adm = 1*3 + 1*2 - 2*0 = 5
        // score = 100 / (1 + 5) = 16.66
        assert!(score > 16.0 && score < 17.0);
    }
}
