/**
 * Represents a single location component within a LocationMatrix object and 
 * stores the location (row and column) and string value of the component.
 * 
 * @property {number} row - The row location of this component
 * @property {number} column - The column location of this component
 * @property {string} value - The string containing the location value associated
 *                            with this component
 * @property {Set<LocationComponent>} links - The other location components that
 *                                          are related / linked to this one
 * 
 */

export class LocationComponent{

    row: number;
    column: number;
    value: string;
    links: Set<LocationComponent> = new Set();

    /**
     * Initializes a LocationComponent with position and optional value.
     * 
     * @param pair - A tuple of (row, column) coordinates for this component's position in the matrix.
     * @param inputValue - The string value of this location component. Defaults to an empty string.
     */
    constructor( public pair: [number, number], public inputValue: string = "" ) {
        this.row = pair[0];
        this.column = pair[1];
        this.value = inputValue;
    };

    /**
     * A check for consistency with the Python version to have similar functionality to Python's
     * checks for truthiness on a class.
     * 
     * @returns true if the 'value' variable is defined or non-empty and false if it doesn't
     */
    booleanCheck(): boolean {
        if (this.value === undefined || this.value === ""){
            return false;
        } else {
            return true;
        };
    };

    /**
     * An override for the toString method the return the value contained in this component
     * as well as it's coordinates.
     * 
     * @returns A formatted string containing the value and (row, column) position
     * 
     * 
     */
    toString(): string {
        return `${this.value} (${this.row}, ${this.column})`;
    }

    /**
     * This is used to compare this LocationComponent with another LocationComponent since
     * TypeScript compares for equality based on location rather than value. As a result,
     * it is not in the Python version.
     * 
     * @param otherLocationComponent - The LocationComponent to compare to this one for 
     *                                 equality
     * 
     * @returns true if both LocationComponent instances have all the same values and false if 
     *          they don't
     */
    equals(otherLocationComponent: LocationComponent): boolean {
        if (this.value !== otherLocationComponent.value){
            return false;
        } else if (this.row !== otherLocationComponent.row){
            return false;
        } else if (this.column !== otherLocationComponent.column){
            return false;
        }
    }

    /**
     * Creates a bidirectional link between this LocationComponent and another LocationComponent.
        All linked components share the same set of links.
     * 
     * @param other -  The LocationComponent to link with
     */
    link(other: LocationComponent): void{

        this.links.add(other);
        other.links.add(this);
        var mergedSet = new Set([...this.links, ...other.links]);
        for (const component of mergedSet){
            component.links = mergedSet;
        };
    };

};