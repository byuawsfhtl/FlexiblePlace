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
     * This is a necessary function for consistency with the Python version. It's necessary so there's a
     * function that can be called that will have similar functionality to Python's checks for truthiness 
     * on a class. It makes it so that if the matrix in the aligner instance is empty, it returns talse. 
     * Otherwise it returns true.
     * 
     * @returns false if the matrix is empty and true if it isn't
     */
    toBoolean(): boolean {
        if (this.matrix !== undefined && this.matrix.length > 0) {
            return true;
        };

        return false;
    };

    /**
     * This is a necessary function for consistency with the Python version. It's necessary so there's a
     * function that can be called that will have similar functionality to Python's ability to print out
     * an object as a string. In accordance with the Python version, this returns a formatted string 
     * representation of the Aligner and renders the matrix as a pipe-separated table with columns aligned 
     * based on the longest value in each column. Note that empty rows result in an empty string.
     * 
     * @returns A formatted string representing the matrix as a table, or an empty string if the matrix is empty
     */
    toString(): string {
        // If no rows, return an empty string
        if (this.matrix === undefined || this.matrix.length < 1){
            return "";
        };
        // Determine the width for each column based on the longest string in that column
        var widths: Array<number> = [];
        for (var columnIndex = 0; columnIndex < this.columnCount; columnIndex++){
            var max_length = 0;
            for (var rowIndex = 0; rowIndex < this.matrix.length; rowIndex++){
                //Guard against rows shorter than column_count (shouldn't happen after resizing)
                if (columnIndex < this.getRow(rowIndex).length){
                    var value;
                    try {
                        value = this.get(rowIndex, columnIndex).value;
                        if (value === undefined){
                            throw new Error();
                        }
                    } catch {
                        value = "";
                    };
                    max_length = Math.max(max_length, value.length);
                };
            };
            widths.push(max_length);
        };
        // Build each row as a pipe-separated string with left-aligned padding
        var lines: Array<string> = [];

        for(var rowIndex=0; rowIndex<this.matrix.length; rowIndex++){
            let cells: Array<string> = [];
            for (var columnIndex = 0; columnIndex < this.columnCount; columnIndex++){
                let val = "";
                if(columnIndex < this.getRow(rowIndex).length){
                    val = this.get(rowIndex,columnIndex).value || "";
                }
                cells.push(val.padEnd(widths[columnIndex]))
            }   
            
            let line =  "| " + cells.join(" | ") + " |";
            lines.push(line)
        }
        return lines.join("\n");


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
     * Return the locations in the matrix as a list of lists of strings.
     * 
     * @returns List of all locations in matrix
     */
    getLocations(): Array<Array<string>>{
        let locations: Array<Array<string>> = [];

        this.matrix.forEach((row: Array<LocationComponent>)=>{
            let locationRow: Array<string> = [];
            row.forEach((location: LocationComponent)=>locationRow.push(location.value))
        })

        return locations;
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
     * Return a column from the matrix as a list of LocationComponent objects.
     * 
     * @param rowIndex - Zero-based column index.
     * 
     * @returns The column components in row order.
     */
    getColumn(columnIndex: number): Array<LocationComponent> {
        let colVals: Array<LocationComponent> = [];
        this.matrix.forEach((row: Array<LocationComponent>)=>colVals.push(row[columnIndex]));
        return colVals;
    }; 

    /***
     * Insert or replace a LocationComponent into the internal matrix at its (row, column).
     * 
     * @param component - The LocationComponent to insert.
     */
    insert(component: LocationComponent){
        let row = component.row;
        let col = component.column;
        this.matrix[row][col]=component;
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
     * Resizes the Aligner to have the specified number of columns by padding rows with empty
     * LocationComponent objects as needed. Updates the column_count to reflect the new size. (Note: cannot
     * be used to make matrix smaller than current size).
     * 
     * @param newSize -  The new number of columns for the matrix
     * 
     */
    private _resize(newSize: number): void {
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

    /**
     * Aligns all rows in an Aligner by finding best matches between components across rows and linking
     * them together. Processes each row sequentially, comparing each unlinked component with components in previous
     * rows to find optimal alignments based on similarity scores.
     */
    align(): void {

        for (let i = 1; i < this.matrix.length; i++) {
            while (true) {
                let match = this._findBestMatch(i);
                if(match.length === 0){
                    break;
                }

                let row_a: number = match[0][0]
                let col_a: number = match[0][1]
                let component_a: LocationComponent = this.get(row_a, col_a)
                
                let row_b: number = match[1][0]
                let col_b: number = match[1][1]
                let component_b: LocationComponent = this.get(row_b, col_b)

                this.link(component_a, component_b)
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
    private _findBestMatch(rowIndex: number): [[number, number], [number, number] ] | []{

        var bestScore: number = 80;
        var bestMatch: [[number, number], [number, number]]  | [] = [];

        for (var columnIndex = 0; columnIndex < this.getRow(rowIndex).length; columnIndex++) {
            const currentComponent: LocationComponent = this.get(rowIndex, columnIndex);
            if (currentComponent.links.size > 0) {
                continue;
            } else {
                [bestScore, bestMatch] = this._compareWithPrevious(currentComponent, bestScore, bestMatch);
            };
        };

        return bestMatch;

    }

    /**
     * Compares the current component with all components in previous rows. If it is a better match then 
     * the previous best, best_match and best_score are updated.
     * 
     * @param currentComponent - The component to find a match for
     * @param bestScore - The score of the best found match for the current component so far
     * @param bestMatch - A pair of coordinate tuples referencing the index locations of the components
     *                    that are currently labelled as the best match, or an empty tuple
     * 
     * @returns A tuple containing the best score that's been found after this function, as well as a
     *          tuple of coordinate tuples containing the index locations of the two components that
     *          match well. This second tuple will be empty if an empty tuple was supplied and no match was found.
     */
    private _compareWithPrevious(currentComponent: LocationComponent, bestScore: number, bestMatch: [[number, number], [number, number]] | []): [number, [[number, number], [number, number]] | []]{

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
     * Links two LocationComponents together by aligning them in the matrix. Moves the closer component
     * to match the column of the farther component, and creates a link between them if the move is legal.
     * Once the components are linked, an attempt to move one of them will the other to move with it.
     * Example:
     *     print(aligner) # Note: the link is marked below with a '%', but will not be in a real print
     *     # |             |             |% washington  %|
     *     # |             | walla walla |% washington  %|
     *     # | walla walla | washington  | united states |
     *     component_a: LocationComponent = aligner.get(2,1) # 'washington' in last row
     *     component_b: LocationComponent = aligner.get(1,0) # 'washington' in 2nd row
     *     aligner.link(component_a, component_b)
     *     print(aligner) # Note: the link is marked below with a '%', but will not be in a real print
     *     # |             |% washington  %|               |
     *     # | walla walla |% washington  %|               |
     *     # | walla walla |% washington  %| united states |
     * 
     * @param component_a - The first component to link.
     * @param component_b - The second component to link.
     */
    link(component_a: LocationComponent, component_b: LocationComponent){
        const [closest_component, farthest_component] = this._order_components(component_a,component_b);
        if(this._illegal_move(closest_component,farthest_component)){
            component_a.link(component_a);
            return;
        }
        const distance: number = farthest_component.column - closest_component.column;
        this._move(farthest_component,distance);
        component_a.link(component_b);
    }

    /**
     * Orders two LocationComponents by their column position, returning the component with the lower column
     * first and the component with the higher column second.
     * @param component_a - the first component
     * @param component_b - the second component.
     * 
     * @returns - A tuple of (closest_to_start, farthest_from_start)
     */
    private _order_components(component_a: LocationComponent, component_b: LocationComponent): [LocationComponent, LocationComponent]{
        throw(new Error("Not implemented"));
    }

    
    /**
     * Checks for an illegal move. A move is illegal if the components being linked together are empty, or if
     * other links in between the components that are being aligned make it impossible to align them.
     * 
     * @param component_a - component closest to the beginning of the row and will be moved
     * @param component_b - component farthest from the beginning of the row and will not move
     * 
     * @returns true if the move is illegal, otherwise false.
     */
    private _illegal_move(component_a: LocationComponent, component_b: LocationComponent): boolean{
        throw(new Error("Not implemented"));
    }

    /**Moves a LocationComponent to the right by the specified distance by repeatedly shifting it one column
     * at a time, resizing the matrix if necessary.
     * 
     * @param component - The component to move.
     * @param distance - The number of columns to move the component to the right.
     */
    private _move(component: LocationComponent, distance: number){
        throw(new Error("Not implemented"));
    }

    /**Shifts a LocationComponent one column to the left in the matrix, resizing the matrix if the component
     *  is at the end. Also recursively shifts all subsequent components in the row and updates linked components.
     * 
     * @param component The component to shift left.
     */
    private _shift_left(component: LocationComponent){
        throw(new Error("Not implemented"));
    }

    /**
     * Return the row indices represented by each component's links.
     * 
     * @returns - A matrix containing linked row indices for each component.
     */
    get_links(): Array<Array<Set<number>>>{
        throw(new Error("Not implemented"));
    }

    /**
     * Convert linked LocationComponents into their row indices.
     * 
     * @param links - The components whose row indices should be returned.
     * 
     * @returns - The row indices represented by the linked components.
     */
    private _repackage_as_ints(links: Set<LocationComponent>): Set<number>{
        throw(new Error("Not implemented"));
    }

};
