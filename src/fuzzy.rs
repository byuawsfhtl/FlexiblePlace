use strsim::levenshtein;

/// Calculates a score based on fuzzy string similarity, as in grail or tt merge score.
pub fn calculate_fuzzy_score(place_a: &str, place_b: &str) -> f64 {
    let mut score = 100.0;

    let place_a_parts: Vec<String> = place_a
        .split(',')
        .map(|part| part.trim().to_lowercase())
        .filter(|part| !part.is_empty())
        .collect();
    
    let place_b_parts: Vec<String> = place_b
        .split(',')
        .map(|part| part.trim().to_lowercase())
        .filter(|part| !part.is_empty())
        .collect();

    let (mut more_detailed, less_detailed) = if place_a_parts.len() > place_b_parts.len() {
        (place_a_parts, place_b_parts)
    } else {
        (place_b_parts, place_a_parts)
    };

    if !less_detailed.is_empty() {
        let mut overlap: Vec<f64> = Vec::new();

        for part in &less_detailed {
            let mut found = false;
            let mut best_this_score = 0.0;

            let mut matched_index = None;

            for (i, other_part) in more_detailed.iter().enumerate() {
                // Calculate similarity ratio
                // Levenshtein distance: d
                // Ratio: (max_len - d) / max_len * 100
                let d = levenshtein(part, other_part);
                let max_len = part.len().max(other_part.len()) as f64;
                let this_score = if max_len > 0.0 {
                    (max_len - d as f64) / max_len * 100.0
                } else {
                    100.0
                };

                if this_score > 80.0 {
                    overlap.push(this_score);
                    matched_index = Some(i);
                    found = true;
                    break;
                }
                
                if this_score > best_this_score {
                    best_this_score = this_score;
                }
            }

            if found {
                if let Some(i) = matched_index {
                    more_detailed.remove(i);
                }
            } else {
                overlap.push(best_this_score);
            }
        }

        if !overlap.is_empty() {
            score = overlap.iter().sum::<f64>() / overlap.len() as f64;
        }
    }

    score
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fuzzy_score_exact() {
        let score = calculate_fuzzy_score("Villepinte, Aude, France", "Villepinte, Aude, France");
        assert!(score > 99.0);
    }

    #[test]
    fn test_fuzzy_score_misspelled() {
        let score = calculate_fuzzy_score("Villepinte, Aude, France", "Vilepinte, Aude, France");
        assert!(score > 80.0);
    }

    #[test]
    fn test_fuzzy_score_different() {
        let score = calculate_fuzzy_score("Villepinte, Aude, France", "Paris, France");
        assert!(score < 80.0);
    }
}
