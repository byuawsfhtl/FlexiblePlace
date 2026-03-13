use rusqlite::{Connection, Result};
use crate::models::{PlaceData, Location};
use serde_json;

pub fn lookup_place(conn: &Connection, place_name: &str) -> Result<Option<PlaceData>> {
    let mut stmt = conn.prepare("SELECT location, placeid FROM places WHERE place = ?1")?;
    let mut rows = stmt.query([place_name])?;

    if let Some(row) = rows.next()? {
        let location_json: String = row.get(0)?;
        let placeid: Option<String> = row.get(1)?;

        let location: Option<Location> = serde_json::from_str(&location_json).ok();

        Ok(Some(PlaceData {
            place: place_name.to_string(),
            location,
            placeid,
        }))
    } else {
        Ok(None)
    }
}

pub fn init_db(db_path: &str) -> Result<Connection> {
    let conn = Connection::open(db_path)?;
    // Assuming the table already exists as per the requirements (SQLite file packaging)
    Ok(conn)
}
