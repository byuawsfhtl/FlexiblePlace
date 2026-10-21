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
 *      locations = [FlexiblePlace("Washington, United States").getLocationComponents,
 *                   FlexiblePlace("Walla Walla, Washingon").getLocationComponents,
 *                   FlexiblePlace("Walla Walla, Washingon, United States").getLocationComponents]
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
            var maxLength = 0;
            for (var rowIndex = 0; rowIndex < this.matrix.length; rowIndex++){
                //Guard against rows shorter than columnCount (shouldn't happen after resizing)
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
                    maxLength = Math.max(maxLength, value.length);
                };
            };
            widths.push(maxLength);
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
     * LocationComponent objects as needed. Updates the columnCount to reflect the new size. (Note: cannot
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

                let rowA: number = match[0][0]
                let colA: number = match[0][1]
                let componentA: LocationComponent = this.get(rowA, colA)
                
                let rowB: number = match[1][0]
                let colB: number = match[1][1]
                let componentB: LocationComponent = this.get(rowB, colB)

                this.link(componentA, componentB)
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
     * the previous best, bestMatch and bestScore are updated.
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
     *     componentA: LocationComponent = aligner.get(2,1) # 'washington' in last row
     *     componentB: LocationComponent = aligner.get(1,0) # 'washington' in 2nd row
     *     aligner.link(componentA, componentB)
     *     print(aligner) # Note: the link is marked below with a '%', but will not be in a real print
     *     # |             |% washington  %|               |
     *     # | walla walla |% washington  %|               |
     *     # | walla walla |% washington  %| united states |
     * 
     * @param componentA - The first component to link.
     * @param componentB - The second component to link.
     */
    link(componentA: LocationComponent, componentB: LocationComponent){
        const [closestComponent, farthestComponent] = this._orderComponents(componentA,componentB);
        if(this._illegalMove(closestComponent,farthestComponent)){
            componentA.link(componentA);
            return;
        }
        const distance: number = farthestComponent.column - closestComponent.column;
        this._move(farthestComponent,distance);
        componentA.link(componentB);
    }

    /**
     * Orders two LocationComponents by their column position, returning the component with the lower column
     * first and the component with the higher column second.
     * @param componentA - the first component
     * @param componentB - the second component.
     * 
     * @returns - A tuple of (closestToStart, farthestFromStart)
     */
    private _orderComponents(componentA: LocationComponent, componentB: LocationComponent): [LocationComponent, LocationComponent]{
        if(componentA.column < componentB.column){
            return [componentA,componentB];
        }
        else{
            return [componentB,componentA];
        }
    }

    
    /**
     * Checks for an illegal move. A move is illegal if the components being linked together are empty, or if
     * other links in between the components that are being aligned make it impossible to align them.
     * 
     * @param componentA - component closest to the beginning of the row and will be moved
     * @param componentB - component farthest from the beginning of the row and will not move
     * 
     * @returns true if the move is illegal, otherwise false.
     */
    private _illegalMove(componentA: LocationComponent, componentB: LocationComponent): boolean{
        if(!componentA.booleanCheck() || !componentB.booleanCheck()){
            return true;
        }
        for(let i = componentA.column; i <= componentB.column; i++){
            const componentToCheck = this.get(componentA.row,i);
            if (Array.from(componentToCheck.links).some(
                component => component.row === componentB.row
            )) {
                return true;
            }
        }
        return false;
    }

    /**Moves a LocationComponent to the right by the specified distance by repeatedly shifting it one column
     * at a time, resizing the matrix if necessary.
     * 
     * @param component - The component to move.
     * @param distance - The number of columns to move the component to the right.
     */
    private _move(component: LocationComponent, distance: number){
        for(let i = 0;i < distance;i++){
            this._shiftLeft(component);
        }
    }

    /**Shifts a LocationComponent one column to the left in the matrix, resizing the matrix if the component
     *  is at the end. Also recursively shifts all subsequent components in the row and updates linked components.
     * 
     * @param component The component to shift left.
     */
    private _shiftLeft(component: LocationComponent){
        const currentColumn: number = component.column;
        if(!component.booleanCheck()){
            return;
        }
        else if(currentColumn === 0){
            this._resize(this.columnCount+1);
            this._shiftLeft(component);
        }
        else{
            let row: number = component.row;
            let column: number = component.column;
            column-=1;
            this._shiftLeft(this.get(row,column));
            component.column-=1;
            this.insert(component);

            component.links.forEach((linkedComponent)=>{
                const distance: number = Math.abs(component.column - linkedComponent.column);
                this._move(linkedComponent,distance);
            })

            this.insert(new LocationComponent([row,component.column+1]));
        }
    }

    /**
     * Return the row indices represented by each component's links.
     * 
     * @returns - A matrix containing linked row indices for each component.
     */
    getLinks(): Array<Array<Set<number>>>{
        let links: Array<Array<Set<number>>> = [];

        this.matrix.forEach((row)=>{
            let linksRow: Array<Set<number>> = [];
            row.forEach((component)=>{
                let curLinks: Set<number>;
                if(component.links.size > 0 || !component.value){
                    curLinks = this._repackageAsInts(component.links);
                }
                else{
                    curLinks = new Set<number>([component.row]);
                }
                linksRow.push(curLinks);
            });
            links.push(linksRow);
        });

        return links;
    }

    /**
     * Convert linked LocationComponents into their row indices.
     * 
     * @param links - The components whose row indices should be returned.
     * 
     * @returns - The row indices represented by the linked components.
     */
    private _repackageAsInts(links: Set<LocationComponent>): Set<number>{
        let linksAsInts = new Set<number>();

        links.forEach((component)=>linksAsInts.add(component.row));

        return linksAsInts;
    }

};
