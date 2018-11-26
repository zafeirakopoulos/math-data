// 2 dimensional tuple

import * as React from "react";
import {InputElement} from "./input-element";

export type Tuple = [number, number];

export class TupleComponent extends React.Component<any, any> {

    // props:
    // tup_dimension = 2
    // tup_elem_types = ["Integer", "Integer"]
    // value = [4, 5]



    render() {
        const tuples = this.props.value.map((elemValue: number, elemIndex: number) => {
            return (
                <InputElement
                    row={this.props.tupleIndex}
                    col={elemIndex}
                    value={elemValue}
                    onChange={this.onChange(elemIndex, elemValue)}
                    key={elemIndex}
                />
            );
        });

        return (<div className="tuple">{tuples}</div>);
    }

    private onChange = (elemIndex, elemValue) => () => {
        this.props.onChange(this.props.tupleIndex, elemIndex, elemValue);
    }
}