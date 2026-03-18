# PlaceComparator

A Rust library for comparing historical places with bindings for Python and TypeScript.

## Core Metrics
- **Physical Distance**: Uses an embedded SQLite database (automatically handled).
- **Administrative Distance**: Based on hierarchical location trees (split by commas).
- **Fuzzy String Matching**: Accounts for misspellings using string similarity ratios.

## Usage

### Python
```python
import placecomparator

# Compare by name
result = placecomparator.compare_places("Villepinte, Aude, France", "Vilepinte, Aude, France")
print(result)

# Compare by JSON data
data1 = '{"place": "Villepinte, Aude, France", "location": {"type": "Point", "coordinates": [2.08, 43.28]}}'
data2 = '{"place": "Vilepinte, Aude, France", "location": {"type": "Point", "coordinates": [2.08, 43.28]}}'
result = placecomparator.compare_places_from_json(data1, data2)
print(result)
```

### TypeScript (Wasm)
```typescript
import { comparePlaces, comparePlacesFromJson } from 'placecomparator';

// Compare by name
const result = comparePlaces("Villepinte, Aude, France", "Vilepinte, Aude, France");
console.log(result);

// Compare by JSON data
const resultJson = comparePlacesFromJson(data1Json, data2Json);
console.log(resultJson);
```

## Installation from GitHub

### Python (pip)
```bash
pip install git+https://github.com/byuawsfhtl/PlaceComparator.git
```

### TypeScript/JavaScript (npm)
To use the WASM package in your JS/TS project:
```bash
npm install https://github.com/byuawsfhtl/PlaceComparator.git
```
Note: You may need to run `wasm-pack build` if you are consuming the repository directly.

## Setup & Build
- **Rust**: `cargo build`
- **Python**: `maturin develop`
- **TypeScript**: `wasm-pack build`
