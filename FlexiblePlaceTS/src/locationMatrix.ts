import { basicComparisonAlgorithm } from "./compareLocationComponents";
import { LocationComponent } from "./locationComponent";

export class LocationMatrix{

    rowCount: number;
    columnCount: number;
    matrix: Array<Array<LocationComponent>>;

    constructor(){
        this.rowCount = 0;
        this.columnCount = 0;
        this.matrix = [];
        AAAAAAAAAAA Unfinished;
    };

    /**
     * A check for consistency with the Python version to have similar functionality to Python's
     * checks for truthiness on a class.
     * 
     * @returns true if the 'matrix' variable is defined or non-empty and false if it doesn't
     */
    booleanCheck(): boolean {
        if (this.matrix === undefined || this.matrix === []){
            return false;
        } else {
            return true;
        };
    };

    /**
     * This is used to compare the matrix inside of this LocationMatrix instance with another
     * input matrix by value. It's not present in the Python version because Python does
     * this by default, while TypeScript and JavaScript don't.
     * 
     * 
     */
    matrixComparisonHelper(otherMatrix: Array<Array<LocationComponent>>): boolean {

            
    }

}