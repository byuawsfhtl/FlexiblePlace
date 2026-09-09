import { LocationComponent } from "./locationComponent";
import { ratio as fuzzball_ratio } from "fuzzball";
import memoize from 'memoizee';

// Note here that memoizee (and the memoize function) is the typescript equivalent of lru cache in python
export const basicComparisonAlgorithm = memoize(basicComparisonAlgorithmUnmemoized, {max:1000});

/**
 * Calculates a score out of 100 of the likelihood that 2 location components refer to the same location. 
 * This is done by taking the fuzzy string score of the two components and then deducting points for these reasons:
 *      1. The strings are short.
 *      2. The strings are misaligned (the algorithm will favor location components that are already aligned).
 * 
 * @param locationOne - The first LocationComponent
 * @param locationTwo - the second LocationComponent
 * 
 * @returns A percent score (float) out of 100
 * 
 */
function basicComparisonAlgorithmUnmemoized(locationOne: LocationComponent, locationTwo: LocationComponent): number{

    var componentOne: string = locationOne.value;
    var componentTwo: string = locationTwo.value;

    if (componentOne === "" || componentTwo === "" || componentOne === undefined || componentTwo === undefined){
        return 0.0;
    };

    var fuzzyScore: number = fuzzball_ratio(componentOne, componentTwo); 
    var deductionForSmallComponentLength: number = 2 ** -(componentTwo.length - 1); // More letters = smaller score deduction
    var misalignment: number = Math.abs(locationOne.column - locationTwo.column);
    var decutionForMisalignment: number = misalignment ** 3; // A street address compared with a country will have a high deduction

    return (fuzzyScore - deductionForSmallComponentLength - decutionForMisalignment);
};