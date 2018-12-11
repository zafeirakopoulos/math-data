import React, {Component} from 'react';
import {flattenObject} from "../util/helpers";

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

        // loop over this.prop.raw. If current item is true in this.prop.raw_types that's our type.
        let type = null;
        for (const key of Object.keys(raw_types)) {
            // console.log(`${key}${raw_types[key]} ${raw[key]} ${raw}`)
            // console.log(key, raw_types[key], raw[key], raw);
            if (raw[key]) {
                type = key;
            }
        }
        const structures = this.parseStructure(raw[type]);
        console.log(structures);
        // loop over this.props.attributes. If value is true, we need to parse "structure" and "element".
        for (const key of Object.keys(attributes)) {
            if (attributes[key]) {

            }
        }

        return (
            <div>
                mathobj
            </div>
        );
    }

    // Checks if a string contains a variable.
    // For example in structure if we got @size.vertices
    // We need to include this.props.size.vertices
    variableFilter = (input: string | number) => {
        if (typeof input === 'string' && input.startsWith('@')) {
            const withoutAtSymbol = input.substring(1);
            return this.state.flatProps[withoutAtSymbol];
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
}

/*
We take option as:
{
  "edges.weighted" = true,
  "edges.directed" = true,
  "vertices.weighted" = true
}

so we want to be able to
*/
function findInOption(key: string) {

}

export default MathObject;
