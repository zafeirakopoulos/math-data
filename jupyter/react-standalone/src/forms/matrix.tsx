import * as React from "react";
import {ValueType} from "../definitions/types";
import {InputElement} from "./input-element";

export interface IMatrixProps {
    row: number,
    col: number,
    elementType: string,
    defaultValue: ValueType
}

export interface IMatrixState {
    row: number,
    col: number,
    data: ValueType[][], // TODO think a better way to do this. Maybe Matrix<T>
}

// Usage: <Matrix row=5 col=5 elementType="boolean" value="0" />
export class Matrix extends React.Component<any, IMatrixState> {
    constructor(props: IMatrixProps) {
        super(props);
        this.state = {
            row: this.props.row,
            col: this.props.col,
            data: this.generateDataState()
        };
    }

    generateDataState(): any[] {
        // Matrix array representation
        const data = [];
        for (let i = 0; i < this.props.row; ++i) {
            data.push([]);
            for (let j = 0; j < this.props.row; ++j) {
                data[i].push(this.props.defaultValue);
            }
        }

        return data;
    }

    // Create inputs as table of InputElement components
    renderInputTable() {
        const table = [];
        for (let i = 0; i < this.props.row; ++i) {
            const children = [];
            for (let j = 0; j < this.props.col; j++) {
                let dataPoint = this.state.data[i][j];
                if (dataPoint === "undefined") {
                    dataPoint = this.props.defaultValue;
                }
                children.push(
                    <td key={j}>
                        <InputElement
                            row={i}
                            col={j}
                            value={dataPoint}
                            onChange={this.handleChange}
                            elementType={this.props.elementType}
                        />
                    </td>
                );
            }
            table.push(<tr key={i}>{children}</tr>);
        }

        return <table>
            <tbody>{table}</tbody>
        </table>;
    }

    render() {
        return (this.renderInputTable());
    }

    // Children will call this callback when their input changes.
    // This updates Matrix components data state.
    // Because we can't access child components inner state, we have to use this callback from parent.
    // By doing that we are setting Matrix component as source of thruth.
    private handleChange = (row: number, col: number, newValue: ValueType) => {
        const copyData = this.state.data.slice();
        copyData[row][col] = newValue;
        this.setState({data: copyData});
        this.props.jsonOutputSetter(copyData);
    };
}