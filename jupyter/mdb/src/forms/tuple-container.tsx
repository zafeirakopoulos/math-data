// Contains group of TupleComponents and manages their state.

import * as React from "react";
import { TupleComponent } from "./tuple-component";

export interface ITupleContainerProps {
    tup_dimension: number
}

// export interface ITupleContainerState {
//
// }

// TODO specify props and state
export class TupleContainer extends React.Component<ITupleContainerProps, any> {

    // props:
    // tup_dimension = 2
    // tup_elem_types = ["Integer", "Integer"]

    // state:
    // values = [ [1,2], [2,3], [3, 4], [4, 5] ]

    constructor(props: any) {
        super(props);

        const nullTuple = [];
        for (let i = 0; i < this.props.tup_dimension; i++) {
            nullTuple.push(0);
        }

        this.state = {
            values: Array(5).fill(nullTuple)
        }
    }

    render() {

        const tuples = this.state.values.map((value) => {
            return(
                <TupleComponent
                    value={this.state.values}
                    defaultValue={0}
                    onChange={}
                />
            )

        });
        
        return ()
    }

    userInputHandler() {
        
    }
}