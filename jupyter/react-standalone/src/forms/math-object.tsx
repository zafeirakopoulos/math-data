// import _ from 'lodash';
// import {graph} from "../definitions/all-definitions";
import React, {Component} from 'react';
import {MathObjectParser} from '../parser/MathObjectParser';
import {flattenObject} from "../util/helpers";

class MathObject extends Component<any, any> {
    private parser: MathObjectParser;
    private parsed: any;

    constructor(props) {
        super(props);
        this.state = {
            flatProps: flattenObject(this.props)
        }
    }

    componentDidMount() {
    }

    // componentDidUpdate(prevProps) {
    //     console.log('componentDidUpdate', this.props);
    //     if (!_.isEqual(this.props, prevProps)) {
    //         this.parser.setObjDefinition(this.props.raw);
    //         this.parsed = this.parser.parse();
    //     }
    // }

    render() {
        const {
            attributes,
            size,
            options,
            raw_types,
            raw,
        } = this.props;

        const parser = new MathObjectParser();
        const setDefinition = parser.setObjDefinition(this.props);
        if (!setDefinition) {
            console.log(`can't set definition, parser:`, parser);
        }
        const result = parser.parse('raw.dense');
        console.log('result', result);
        // var sparseVert = this.parser.parse();

        return "";
    }
}

export default MathObject;
