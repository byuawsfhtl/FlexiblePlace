use rusqlite::{Connection, Result};
use crate::models::{PlaceData, Location};
use std::io::{Read, Write};
use flate2::read::GzDecoder;
use tempfile::NamedTempFile;
use std::sync::OnceLock;
use std::path::PathBuf;

static DB_PATH: OnceLock<PathBuf> = OnceLock::new();

const DB_BYTES: &[u8] = include_bytes!("places.db.gz");

pub fn init_db(_path: &str) -> Result<Connection> {
    let path = DB_PATH.get_or_init(|| {
        let mut decoder = GzDecoder::new(DB_BYTES);
        let mut buffer = Vec::new();
        decoder.read_to_end(&mut buffer).expect("Failed to decompress database");
        
        let mut file = NamedTempFile::new().expect("Failed to create temp file");
        file.write_all(&buffer).expect("Failed to write to temp file");
        
        // Persist the file so it doesn't get deleted when NamedTempFile is dropped
        let (_, path) = file.keep().expect("Failed to persist temp file");
        path
    });

    Connection::open(path)
}

pub fn lookup_place(conn: &Connection, place_name: &str) -> Result<Option<PlaceData>> {
    let mut stmt = conn.prepare("SELECT latitude, longitude, placeid FROM places WHERE place = ?1")?;
    let mut rows = stmt.query([place_name])?;

    if let Some(row) = rows.next()? {
        let lat: f64 = row.get(0)?;
        let lon: f64 = row.get(1)?;
        let placeid: Option<String> = row.get(2)?;

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

    #[test]
    fn test_db_init_and_lookup_schema() {
        let conn = init_db("").expect("Failed to init DB");
        let mut stmt = conn.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='places'").expect("Query failed");
        let mut rows = stmt.query([]).expect("Query failed");
        assert!(rows.next().expect("No table found").is_some());
    }

    #[test]
    fn test_lookup_real_place() {
        let conn = init_db("").expect("Failed to init DB");
        
        // Use exact string with quotes as found in database
        let place_name = "\"Ann Arbor\"";
        let result = lookup_place(&conn, place_name).expect("Lookup failed");
        
        assert!(result.is_some(), "Place '\"Ann Arbor\"' should exist in the database");
        let data = result.unwrap();
        assert_eq!(data.place, place_name);
        assert!(data.location.is_some());
        
        let loc = data.location.unwrap();
        // Coordinates for Ann Arbor are roughly [-83.7, 42.2]
        // lon = -83.74847, lat = 42.2821
        assert!(loc.coordinates[0] < -80.0 && loc.coordinates[0] > -90.0);
        assert!(loc.coordinates[1] > 40.0 && loc.coordinates[1] < 45.0);
    }

    #[test]
    fn test_lookup_nonexistent_place() {
        let conn = init_db("").expect("Failed to init DB");
        let result = lookup_place(&conn, "This Place Definitely Does Not Exist 12345").expect("Lookup failed");
        assert!(result.is_none());
    }
}
