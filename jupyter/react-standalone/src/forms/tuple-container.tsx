// Contains group of TupleComponents and manages their state.

import * as React from "react";
import {InputElement} from "./input-element";
import {TupleComponent} from "./tuple-component";

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

        const tuples = [];

        for (let i = 0; i < 5; i++) {
            tuples.push([]);
            for (let j = 0; j < this.props.tup_dimension; j++) {
                tuples[i].push(0);
            }
        }

        this.state = {
            values: tuples
        };
    }

    render() {
        // const tuples = this.state.values.map((value: any, index: number) => {
        //     return (
        //         <TupleComponent
        //             value={this.state.values[index]}
        //             defaultValue={0}
        //             key={index}
        //             tupleIndex={index}
        //             onChange={this.handleChange}
        //         />
        //     );
        // });

        const tuples = [];
        const rowlen = this.state.values.length;
        for (let i = 0; i < rowlen; i++) {
            const row = this.state.values[i];

            for (let j = 0; j < this.state.values[i].length; j++) {
                const dataPoint = this.state.values[i][j];
                tuples.push(
                    <InputElement
                        key={`${i},${j}`}
                        row={i}
                        col={j}
                        value={dataPoint}
                        onChange={this.handleChange}
                    />

                );
            }

            tuples.push(<br/>);
        }

        tuples.push(<button onClick={this.print}>Console</button>);
        return tuples;
    }

    print = () => {
        console.log(this.state.values);
    }


    handleChange = (tupleIndex: number, elemIndex: number, value: any) => {
        const copy = this.state.values.slice();
        copy[tupleIndex][elemIndex] = value;
        this.setState({values: copy});
    };
}