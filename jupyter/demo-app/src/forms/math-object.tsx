// import _ from 'lodash';
// import {graph} from "../definitions/all-definitions";
import React, {Component} from 'react';
import {MathObjectParser} from '../parser/MathObjectParser';
import {flattenObject} from "../util/helpers";
import {render} from "react-dom";

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
        const setDefinition = parser.setObjDefinition({
            attributes,
            size,
            options,
            raw_types,
            raw,
        });
        parser.setOrigDefinition(this.props.definition);
        if (!setDefinition) {
            console.log(`can't set definition, parser:`, parser);
        }
        const result = parser.parse('raw.dense');
        console.log('result', result);
        // var sparseVert = this.parser.parse();

        const renderResult = [];

        for (const value of Object.values(result)) {
            // subKey might be "edges" or "vertices" for graph, or "vertices", "rays", "lines" for polyhedron
            for (const [subKey, collectionOfElements] of Object.entries(value)) {
                renderResult.push(<div key={subKey}>{subKey}</div>);

                const dimensions = arrDimension(collectionOfElements);
                if (dimensions.length == 1) {
                    const table = []; // renderResult.push(<table>);
                    for (const elem of Object.values(collectionOfElements)) {
                        table.push(<tr>
                            <td>{elem}</td>
                        </tr>);
                    }

                    renderResult.push(<table className="table ">{table}</table>);
                } else if (dimensions.length == 2) {
                    // renderResult.push(result.map((res, index) => <div key={index}>{res}</div>));

                    const table = []; // renderResult.push(<table>);
                    for (const elem of Object.values(collectionOfElements)) {
                        const tr = [];
                        for (const elem2 of elem) {
                            tr.push(<td>{elem2}</td>);
                        }
                        table.push(<tr>{tr}</tr>);
                    }

                    renderResult.push(<table className="table">{table}</table>);
                } else {
                    // renderResult.push(<div>higher order!</div>);
                }
            }
        }

        return <div>{renderResult}</div>;

        // const dimensions = arrDimension(result);
        // const finalResult = [];
        // if (dimensions.length == 1) {
        //     finalResult.push(result.map((res, index) => <div key={index}>{res}</div>));
        // } else if (dimensions.length == 2) {
        //     finalResult.push(result.map((res, index) => <div key={index}>{res}</div>));
        // } else {
        //     <div></div>
        // }

        // return result.map((res, index) => <div key={index}>{res}
        //     <hr/>
        // </div>);
    }
}

function arrDimension(arr) {
    const dim = [];
    for (; ;) {
        dim.push(arr.length);

        if (Array.isArray(arr[0])) {
            arr = arr[0];
        } else {
            break;
        }
    }
    return dim;
}

export default MathObject;
