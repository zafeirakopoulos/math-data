import _ from 'lodash';

export class MathObjectParser {
    constructor(objDefinition) {
        this.objDefinition = objDefinition;
    }

    static hasSEPair(obj) {
        return obj.hasOwnProperty('structure') && obj.hasOwnProperty('element');
    }

    static hasConditional(obj) {
        return _.includes(_.keys(obj), 'if', 'then', 'else');
    }

    static elementComponent(type, index, ...options) {
        return `<element type="${type}" index="${index}" />`;
    }

    /**
     * Parse given argument as "size".
     * This means if we got a string as parameter, we find and replace it with a number.
     * @param {string[]|string|number} arg Parameter we want to convert to size.
     * @returns {number|number[]}
     */
    sizeParser(arg) {
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

        throw new Error("sizeParser: can't parse this argument: " + arg);
    }

    /**
     * Parse a mathematical object
     *
     * @param {Object} objDef Object definition to parse.
     * @param {string[]} attrArr List of attributes that defines this object's structure.
     * @returns {Array} Array of UI components
     */
    parseObject(attrArr) {
        return this.parseStructureElementPair(_.at(this.objDefinition, attrArr), []);
    }

    /**
     * Parse conditional configuration.
     *
     * @param {Object} obj The object that contains if, then, else statements
     * @returns {Object} structure & element pair
     */
    parseConditional(obj) {
        const ifStmt = obj.if;

        const conditionResult = _.map(ifStmt, (boolean, expression) => {
            const booleanExpression = _
                .at(this.objDefinition, expression.slice(1))[0] === 'true';
            return booleanExpression === boolean;
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
     * @param {Array} prevSizes If this is a recursive structure we need to hold previous sizes to "nest" and "index" UI components
     * @returns {*} Array of UI components
     */
    parseStructureElementPair(elem, prevSizes) {
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

        const dimension = this.sizeParser(sizeArr[0]);
        // console.log('dim', dimension);

        const nextSizeArr = sizeArr.slice(1);
        const result = [];

        // element.type is array
        if (_.isArray(type)) {
            for (var i = 0; i < dimension; i++) {
                if (sizeArr.length > 1) {
                    result.push(this.elementLoop(element, nextSizeArr, [...parentSizes, i]));
                } else {
                    result.push(MathObjectParser.elementComponent(type[i], [...parentSizes, i]));
                }
            }
        } else {
            for (var i = 0; i < dimension; i++) {
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
