use crate::models::{PlaceData, Location};
use std::io::{Read, Write};
use flate2::read::GzDecoder;
use tempfile::NamedTempFile;
use std::sync::OnceLock;
use sqlx::sqlite::SqlitePool;

static DB_POOL: OnceLock<SqlitePool> = OnceLock::new();

const DB_BYTES: &[u8] = include_bytes!("places.db.gz");

async fn get_pool() -> &'static SqlitePool {
    if let Some(pool) = DB_POOL.get() {
        return pool;
    }

    let mut decoder = GzDecoder::new(DB_BYTES);
    let mut buffer = Vec::new();
    decoder.read_to_end(&mut buffer).expect("Failed to decompress database");
    
    let mut file = NamedTempFile::new().expect("Failed to create temp file");
    file.write_all(&buffer).expect("Failed to write to temp file");
    
    let (_, path) = file.keep().expect("Failed to persist temp file");
    let path_str = path.to_str().expect("Path is not valid UTF-8");
    let url = format!("sqlite:{}", path_str);
    
    let pool = SqlitePool::connect(&url).await.expect("Failed to connect to database");
    DB_POOL.get_or_init(|| pool);
    DB_POOL.get().unwrap()
}

pub async fn lookup_place(place_name: &str) -> Result<Option<PlaceData>, String> {
    let pool = get_pool().await;
    
    let result = sqlx::query_as::<_, (f64, f64, Option<String>)>(
        "SELECT latitude, longitude, placeid FROM places WHERE place = ?"
    )
    .bind(place_name)
    .fetch_optional(pool)
    .await
    .map_err(|e| e.to_string())?;

    if let Some((lat, lon, placeid)) = result {
        let location = Some(Location {
            r#type: "Point".to_string(),
            coordinates: vec![lon, lat],
        });

        Ok(Some(PlaceData {
            place: place_name.to_string(),
            location,
            placeid,
        }))
    } else {
        Ok(None)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio;

    #[tokio::test]
    async fn test_db_init_and_lookup() {
        let place_name = "\"Ann Arbor\"";
        let result = lookup_place(place_name).await.expect("Lookup failed");
        assert!(result.is_some());
    }
}
