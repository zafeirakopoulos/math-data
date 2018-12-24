import React, {Component} from 'react';
import {countProperties, flattenObject} from "../util/helpers";
import {InputElement} from "./input-element";

class MathObject extends Component<any, any> {


    constructor(props) {
        super(props);
        this.state = {
            flatProps: flattenObject(this.props)
        }
    }


    render() {
        const {
            attributes,
            size,
            options,
            raw_types,
            raw,
        } = this.props;

        // console.log('size: ', size);

        // loop over this.prop.raw. If current item is true in this.prop.raw_types that's our type.
        let type = null;
        for (const key of Object.keys(raw_types)) {
            if (raw[key]) {
                type = key;
            }
        }

        // Representation of the object
        const repr = [];

        // Structure defines this objects representation
        const structures = this.parseStructure(raw[type]);
        const element = this.parseElement(raw[type]);
        console.log(element);
        console.log(structures);
        for (const key of Object.keys(structures)) {
            // How many dimensions this structure has
            const description = (<caption>{type} - {key}</caption>);
            const dimensionCount = structures[key].length;
            const firstDimension = structures[key][0];
            const currentElement = element[key];
            const vector = [];
            for (let i = 0; i < firstDimension; ++i) {
                if (dimensionCount == 1) { // This is a vector
                    vector.push(<tr><td>{currentElement(i)}</td></tr>);
                } else if (dimensionCount == 2) { // This is a matrix
                    const secondDimension = structures[key][1];
                    const innerElems = [];
                    for (let j = 0; j < secondDimension; ++j) {
                        innerElems.push(<td>{currentElement(i, j)}</td>);
                    }
                    vector.push(<tr>{innerElems}</tr>);
                }
            }

            repr.push(<table>{description}{vector}</table>);
        }


        // console.log(structures);

        // loop over this.props.attributes. If value is true, we need to parse "structure" and "element".
        // for (const key of Object.keys(attributes)) {
        //     if (attributes[key]) {
        //
        //     }
        // }

        return (<div>{repr}</div>);
    }

    // Checks if a string contains a variable.
    // For example in structure if we got @size.vertices
    // We need to include this.props.size.vertices
    variableFilter = (input: string | number) => {
        if (typeof input === 'string' && input.startsWith('@')) {
            const withoutAtSymbol = input.substring(1);
            const asStr = this.state.flatProps[withoutAtSymbol];
            return Number(asStr);
        }

        return input;
    };

    // parse (structure, element) pairs
    parseStructure = (hasStructure: object) => {
        const objs = {};
        for (const key of Object.keys(hasStructure)) {
            if (hasStructure[key] && this.props.attributes.hasOwnProperty(key) && this.props.attributes[key] === true) {
                const structure: string[] = hasStructure[key].structure;
                // console.log('structure', structure);
                const map = structure.map(this.variableFilter);
                // console.log('parseStructure', key, map);
                objs[key] = map;
            }
        }

        // TODO recurse if hasStructure.element has structure inside

        return objs;
    };

    parseElement = (hasElement: object) => {
        const objs = {};
        for (const key of Object.keys(hasElement)) {
            if (hasElement[key] && this.props.attributes.hasOwnProperty(key) && this.props.attributes[key] === true) {
                const element = hasElement[key].element;
                let conditionResolved = null;

                if (element.hasOwnProperty('type')) {
                    if (element.type == "Number") {
                        const defaultValue = element.default ? element.defaultValue : 0;
                        objs[key] = (row) => (<InputElement defaultValue={defaultValue} onChange={this.props.onChange} row={row} col={0}/>);
                    }
                } else if (element.hasOwnProperty('if')) {
                    const condition = Object.keys(element.if)[0];
                    conditionResolved = this.variableFilter(condition);
                    const defaultValue = element.default ? element.defaultValue : 0;
                    const elems = element.then.element.type;
                    objs[key] = elems.map((val, index) => {
                        return (row, col) => {
                            console.log('row, col: ', row, col);
                            return (<InputElement key={key+'-'+index} defaultValue={defaultValue} constraint={val} onChange={this.props.onChange} row={row} col={col}/>);
                        }
                    });
                }
            }
        }

        return objs;
    };
}

export default MathObject;
