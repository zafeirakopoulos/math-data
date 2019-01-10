import _ from 'lodash';

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
            return true;
        } else {
            console.log('given objDef doesnt have some attributes required: ', objDef);
            return false;
        }
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

        return _.flatMap(this.objDefinition.raw_types, (val, key) =>
            _.map(this.objDefinition.raw[key], (objToParse) =>
                this.parseStructureElementPair(objToParse))
        )

        // return this.parseStructureElementPair(this.objDefinition.raw.dense.edges);
    }

    static hasSEPair(obj) {
        return obj.hasOwnProperty('structure') && obj.hasOwnProperty('element');
    }

    static hasConditional(obj) {
        return _.includes(_.keys(obj), 'if', 'then', 'else');
    }

    static elementComponent(type, index, ...options) {
        return `<input type="${type}" index="${index}" />`;
    }

    /**
     * Parse given argument as "size".
     * This means if we got a string as parameter, we find and replace it with a number.
     * @param {string[]|string|number} arg Parameter we want to convert to size.
     * @returns {number|number[]}
     */
    variableParser(arg) {
        if (_.isArray(arg)) {
            return arg.map(currentSize => {
                return _.toNumber(
                    currentSize.startsWith('@') ?
                        _.at(this.objDefinition, currentSize.slice(1))[0] :
                        currentSize);
            });
        }

        if (_.isString(arg)) {
            return _.toNumber(
                arg.startsWith('@') ?
                    _.at(this.objDefinition, arg.slice(1))[0] :
                    arg);
        }

        if (_.isNumber(arg)) {
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

        const conditionResult = _.map(ifStmt, (booleanExpr, expression) => {
            const booleanExpression = _
                .at(this.objDefinition, expression.slice(1))[0] === 'true';
            return booleanExpression === booleanExpr;
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
                    result.push(this.elementLoop(element, nextSizeArr, [...parentSizes, i]));
                } else {
                    result.push(MathObjectParser.elementComponent(type, [...parentSizes, i]));
                }
            }
        }

        return result;
    }
}
