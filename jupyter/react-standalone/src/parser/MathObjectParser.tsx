import _ from 'lodash';
import React from 'react';
import {InputElement} from "../forms/input-element"; // For returning JSX elements from elementComponent method
/**
 * Author: M. Oguzhan Ataman
 * Description:
 * This class is for parsing "MathData" objects.
 * Rules for parsing these objects are defined as "MathDataLanguage"
 *
 * This class designed to return UI components after parsing.
 *
 * We don't store any state except object definition. So we can give new definition by calling setObjDefinition and
 * call parse function on it.
 */
export class MathObjectParser {
    // Static methods
    /**
     * Checks if obj has structure and element pair.
     */
    static hasSEPair(obj): boolean {
        return obj.hasOwnProperty('structure') && obj.hasOwnProperty('element');
    }

    static hasConditional(obj): boolean {
        const objKeys = _.keys(obj);
        return _.every(['if', 'then', 'else'], expr => {
            return _.includes(objKeys, expr);
        });
        // return _.includes(_.keys(obj), 'if', 'then', 'else');
    }

    static elementComponent(type, index, ...options): JSX.Element {
        return <InputElement type={type} index={index} key={index}/>;
    }

    // Class Fields
    private objDefinition;
    private origDefinition;

    // Instance methods
    /**
     * Sets object definition
     *
     * @param objDef The object definition. It should have at least these fields:
     *               "attributes", "options", "raw_types", "size", "raw"
     *               This class expects to filled out fields, for example:
     *               for graphs "attributes.edges": "Boolean", so this class expects a boolean value from user.
     *               All fields except "raw" expected to filled by user.
     */
    setObjDefinition(objDef) {
        const hasAllFields = ['attributes', 'options', 'raw_types', 'size', 'raw'].every(elem => _.has(objDef, elem));
        if (hasAllFields) {
            this.objDefinition = objDef;
            console.log('objDefinition is: ', this.objDefinition);
            return true;
        } else {
            console.log('given objDef doesnt have some attributes required: ', objDef);
            return false;
        }
    }

    setOrigDefinition(origDef) {
        this.origDefinition = origDef;
        this.origDefinition.raw = {};
    }

    /**
     * Parse a mathematical object
     *
     * @param parsePath Where to parse. We can partially parse.
     *                  By default it parses "raw" field which contains structure and element pairs.
     * @returns {Array} Array of UI components
     */
    parse(parsePath = 'raw.dense') {
        // const objectsToParse = _.at(this.objDefinition, parsePath)[0];
        // return _.map(objectsToParse, obj => {
        //     console.log('obj', obj);
        //     this.parseStructureElementPair(obj);
        // });

        const parseResults = [];
        for (const [key] of Object.entries(this.objDefinition.raw_types)) {
            for (const innerKey of Object.keys(this.objDefinition.raw[key])) {
                console.log('innerKey: ', innerKey);
                parseResults.push({
                    [innerKey]: this.parseStructureElementPair(this.objDefinition.raw[key][innerKey])
                });
            }
        }
        // this.preprocess();
        return parseResults;
    }

    /**
     * Replace variable declarations with actual values.
     */
    // preprocess() {
    //     const regex = /"(\w+)*":\s*"(@\w+(\.\w+)*)"/g;
    //
    //     const objString = JSON.stringify(this.origDefinition);
    //
    //     let m = regex.exec(objString);
    //     while (m !== null) {
    //         // This is necessary to avoid infinite loops with zero-width matches
    //         if (m.index === regex.lastIndex) {
    //             regex.lastIndex++;
    //         }
    //
    //         console.log('match', m);
    //
    //         const lhs = m[1];
    //         const rhs = m[2];
    //
    //         // The result can be accessed through the `m`-variable.
    //         // m.forEach((match, groupIndex) => {
    //         //     console.log(`Found match, group ${groupIndex}: ${match}`);
    //         // });
    //         m = regex.exec(objString)
    //     }
    // }

    /**
     * Parse given argument as "size".
     * This means if we got a string as parameter, we find and replace it with a number.
     * @param {string[]|string|number} arg Parameter we want to convert to size.
     * @returns {number|number[]}
     */
    variableParser(arg) {
        console.log('objDef: ', this.objDefinition);
        if (_.isArray(arg)) {
            const parsedVariable = arg.map(currentSize => {
                const toNumber = _.toNumber(
                    currentSize.startsWith('@') ?
                        _.at(this.objDefinition, currentSize.slice(1))[0] :
                        currentSize);
                console.log('XYZ', _.at(this.objDefinition, currentSize.slice(1))[0]);
                console.log('toNumber', toNumber);
                return toNumber;
            });
            console.log('parsedVariable', parsedVariable);
            return parsedVariable;
        }

        if (typeof arg === 'string') {
            return _.toNumber(
                arg.startsWith('@') ?
                    _.at(this.objDefinition, arg.slice(1))[0] :
                    arg);
        }

        if (typeof arg === 'number') {
            return arg;
        }

        throw new Error("variableParser: can't parse this argument: " + arg);
    }

    /**
     * Parse conditional configuration.
     *
     * @param {Object} obj The object that contains if, then, else statements
     * @returns {Object} structure & element pair
     */
    parseConditional(obj) {
        const ifStmt = obj.if;

        const conditionResult = _.map(ifStmt, (localExpr, expression) => {
            const booleanExpression = _.at(this.objDefinition, expression.slice(1))[0] === 'true';
            return booleanExpression === localExpr;
        })[0];

        if (conditionResult) {
            return obj.then;
        }

        const hasElseIf = obj.else.hasOwnProperty('if');
        if (hasElseIf) {
            return this.parseConditional(obj.else);
        }

        return obj.else;
    }

    /**
     * Parse a single structure & element pair, create necessary UI components.
     *
     * @param {Object} elem Object that contains structure and element
     * @param {Array} prevSizes If this is a recursive structure we need to hold previous sizes to "nest" and "index"
     *                UI components. By default it is empty array.
     * @returns {*} Array of UI components
     */
    parseStructureElementPair(elem, prevSizes = []) {
        if (typeof elem !== 'object') {
            return elem;
        } else if (MathObjectParser.hasSEPair(elem)) {
            const sizes = elem.structure;
            const newSizes = _.isUndefined(prevSizes) ? sizes : [...prevSizes, ...sizes];

            // Element has if statement
            if (MathObjectParser.hasConditional(elem.element)) {
                return this.parseStructureElementPair(this.parseConditional(elem.element), newSizes);
            }

            // Element has nested element & structure pair
            if (MathObjectParser.hasSEPair(elem.element)) {
                // return parseSE(elem.element);
                return this.parseStructureElementPair(elem.element, newSizes)
            }

            const element = elem.element;
            return this.elementLoop(element, newSizes, []);
        }

        throw new Error("argument must be a js object and contain structure and element keys");
    }

    /**
     * Create element with nested structure.
     *
     * For example:
     * Lets assume we have sizeArr of [7, 8, 9]
     * This function creates 3 dimensional array (sizeArr.length)
     * array dimensions are 7, 8 and 9
     * every element will be specified by "element" parameter, and will be created with correct indexings so we access easily
     *
     * But if our element's type is an array, last dimension size will be special.
     * They will be related to each other. For example:
     * We have structure [3] and element.type = [Integer, Integer, Number]
     * Every element in this structure will correspond to these types.
     *
     * @param element
     * @param sizeArr
     * @param parentSizes
     * @returns {Array}
     */
    elementLoop(element, sizeArr, parentSizes) {
        const type = element.type;
        const dimension = this.variableParser(sizeArr[0]);

        const nextSizeArr = sizeArr.slice(1);
        const result = [];

        let i;
        console.log('type is: ', type);
        console.log('dimension is: ', dimension);
        console.log('sizeArr is: ', sizeArr);
        // element.type is array
        if (_.isArray(type)) {
            for (i = 0; i < dimension; i++) {
                if (sizeArr.length > 1) {
                    result.push(this.elementLoop(element, nextSizeArr, [...parentSizes, i]));
                } else {
                    result.push(MathObjectParser.elementComponent(type[i], [...parentSizes, i]));
                }
            }
        } else {
            for (i = 0; i < dimension; i++) {
                if (sizeArr.length > 1) {
                    console.log('in 1');
                    result.push(this.elementLoop(element, nextSizeArr, [...parentSizes, i]));
                } else {
                    console.log('in 2');
                    result.push(MathObjectParser.elementComponent(type, [...parentSizes, i]));
                }
            }
        }

        return result;
    }
}
