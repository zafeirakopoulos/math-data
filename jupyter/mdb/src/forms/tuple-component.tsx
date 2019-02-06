// 2 dimensional tuple

import * as React from "react";
import { InputElement } from "./input-element";

export type Tuple = [number, number];

export class TupleComponent extends React.Component<any, any> {

    // props:
    // tup_dimension = 2
    // tup_elem_types = ["Integer", "Integer"]
    // value = [4, 5]


    render() {
        const tuples = this.props.value.map((singleElem: number[], index: number) => {
            return <InputElement value={singleElem} key={index}/>;
        });

        return tuples;
    }
}