import "./compareLocationComponents"
import { basicComparisonAlgorithm } from "./compareLocationComponents";
import { LocationComponent } from "./locationComponent"

/**
 * A class that represents a table of location components, where each row corresponds to the string array of a 
 * FlexiblePlace object and each cell corresponds to a location component (e.g. city, county state/province, 
 * country). This class is used to align locations for comparison, ensuring that each component is compared
 * with the correct component in other locations. Rows are ordered by length.
 *  
 * Example:
 *      locations = [FlexiblePlace("Washington, United States").get_location_components,
 *                   FlexiblePlace("Walla Walla, Washingon").get_location_components,
 *                   FlexiblePlace("Walla Walla, Washingon, United States").get_location_components]
 *      aligner = Aligner(locations)
 *      print(aligner) 
 * | walla walla | washington | united states |
 * |             | washington | united states |
 * | walla walla | washington |               |
 * 
 */
class Aligner {

    rowCount: number;
    columnCount: number;
    matrix: Array<Array<LocationComponent>>;

    constructor(locations: Array<Array<string>>){

        this.rowCount = 0;
        this.columnCount = 0;
        this.matrix = [];
        this.loadPlaces(locations.toSorted((a, b) => a.length - b.length));

    }

    /**
     * Populates the Aligner with location components from a list of place component lists.
     * Converts each string component into a LocationComponent object and adds it to the matrix. Automatically
     * resizes the matrix to accommodate all components, ensuring all rows have the same number of columns.
     * 
     * @param places (list[list[str]]): A list of place component lists, where each inner list represents
     *                                  the components of a single location (e.g., [["123 Main St", "Springfield", 
     *                                  "IL", "USA"]]). 
     * 
     * 
     */
    loadPlaces(places: Array<Array<string>>): void {

        for (const [row, place] of places.entries()) {
            var currentLocationComponents: Array<LocationComponent> = []
            for (const [column, component] of place.entries()) {
                currentLocationComponents.push(new LocationComponent([row, column], component));
            }
            this.matrix.push(currentLocationComponents);
            if (currentLocationComponents.length > this.columnCount){
                this._resize(currentLocationComponents.length);
            } else if (currentLocationComponents.length < this.columnCount){
                this._resize(this.columnCount);
            };
        this.rowCount = this.matrix.length;
        };
    };

    /**
     * Return the LocationComponent at the specified row and column.
     * 
     * @param row - The index of the row to get an item from
     * @param column - The index of the column from which to get an item from in the row
     * 
     * @returns The LocationComponent instance at the specified location
     */
    get(row: number, column: number): LocationComponent {
        return this.matrix[row][column];
    }

    /**
     * Return an entire row of LocationComponent objects.
     * 
     * @param rowIndex - The index of the row to get
     * 
     * @returns A list of LocationComponent objects in the row
     */
    getRow(rowIndex: number): Array<LocationComponent> {
        return this.matrix[rowIndex];
    };

    /**
     * Aligns all rows in an Aligner by finding best matches between components across rows and linking
     * them together. Processes each row sequentially, comparing each unlinked component with components in previous
     * rows to find optimal alignments based on similarity scores.
     */
    align(): void {

        for (let i = 1; i < this.matrix.length; i++) {
            while (true) {
                var match = this.
            }
        }

    }

    /**
     * Finds the best matching pair of LocationComponents between the specified row and all previous rows in
     * the matrix. Compares each unlinked component in the row with all components in previous rows, returning the
     * pair with the highest similarity score above a threshold of 80.0. Returns an empty tuple if no match is found.
     * 
     * @param row - The row index to find matches for
     * 
     * @returns A tuple of two coordinate tuples ((row, col), (row, col)) representing the best matching components, 
     *          or an empty tuple if no match above threshold is found
     */
    _findBestMatch(rowIndex: number): [[number, number], [number, number]]{

        var bestScore: number = 80;
        var bestMatch: [[number, number], [number, number]];

        for (var columnIndex = 0; columnIndex < this.getRow(rowIndex).length; columnIndex++) {
            const currentComponent: LocationComponent = this.get(rowIndex, columnIndex);
            if (currentComponent.links.size > 0) {
                continue;
            } else {
                [bestScore, bestMatch] = this._compareWithPrevious(currentComponent, bestScore, bestMatch);
            };
        };

        return bestMatch;

        // WARNINGS: LOTS OF ISSUES. READ YOUR COMMENTS AND FIX THE SQUIGGLY LINES

        // Okay, so the problem with the original implementation in Python is probably
        // the naming now that I've looked at it for a long time. Rather than calling
        // anything 'column', I think it will be more clear to say index_of_location_name_in_component
        // I would also rename the input variable 'row' to 'row_index' like is done here

        // Update to this: I think that calling it 'column' is fine as long as it's clarified that
        // the 'column' field represents the index of location names within a 'row' item, which should
        // also be labelled as a single location. Ehhhh.... or maybe both should just be renamed? Something
        // needs to change in the documentation though

    }

    /**
     * Compares the current component with all components in previous rows. If it is a better match then 
     * the previous best, best_match and best_score are updated.
     * 
     * @param currentComponent - The component to find a match for
     * @param bestScore - The score of the best found match for the current component so far
     * @param bestMatch - A pair of coordinate tuples referencing the index locations of the components
     *                    that are currently labelled as the best match
     * 
     * @returns A tuple containing the best score that's been found after this function, as well as a
     *          tuple of coordinate tuples containing the index locations of the two components that
     *          match well
     */
    _compareWithPrevious(currentComponent: LocationComponent, bestScore: number, bestMatch: [[number, number], [number, number]]): [number, [[number, number], [number, number]]]{

        var row: number = currentComponent.row;
        var column: number = currentComponent.column;

        for (var i = 0; i < row; i++){
            for (var j = 0; j < this.columnCount; j++) {
                var componentToCompareTo = this.get(i, j);
                var score: number = basicComparisonAlgorithm(currentComponent, componentToCompareTo);
                if (score > bestScore) {
                    bestScore = score;
                    bestMatch = [[row, column], [i, j]];
                };
            };
        };
        return [bestScore, bestMatch];
    };

    /**
     * Resizes the Aligner to have the specified number of columns by padding rows with empty
     * LocationComponent objects as needed. Updates the column_count to reflect the new size. (Note: cannot
     * be used to make matrix smaller than current size).
     * 
     * @param newSize -  The new number of columns for the matrix
     * 
     */
    _resize(newSize: number): void {
        for (const [i, row] of this.matrix.entries()){
            while (row.length < newSize) {
                for (const component of row) {
                    component.column = component.column + 1;
                };
                row.splice(0, 0, new LocationComponent([i, 0]));
            };
        };
        this.columnCount = newSize;
    };

}