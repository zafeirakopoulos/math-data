import * as React from "react";
import { ValueType } from "../definitions/types";
import { InputElement } from "./input-element";


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
export class Matrix extends React.Component<IMatrixProps, IMatrixState> {
    constructor(props: IMatrixProps) {
        super(props);

        this.initDataMatrix();
    }

    initDataMatrix(firstTime = true) {
        // Matrix array representation
        const data = [];
        for (let i = 0; i < this.props.row; ++i) {
            data.push([]);
            for (let j = 0; j < this.props.row; ++j) {
                data[i].push(this.props.defaultValue);
            }
        }

        // On first call, initialize state. Else, only setState data
        if (firstTime) {
            this.state = {
                row: this.props.row,
                col: this.props.col,
                data
            };
        } else {
            this.setState({ data });
        }
    }

    // Create inputs as table of InputElement components
    createInputTable() {
        const table = [];
        for (let i = 0; i < this.props.row; ++i) {
            const children = [];
            for (let j = 0; j < this.props.col; j++) {
                let dataPoint = this.state.data[i][j];
                if (dataPoint === 'undefined') {
                    dataPoint = this.props.defaultValue;
                }
                children.push(
                    <td key={j}>
                        <InputElement
                            row={i}
                            col={j}
                            value={dataPoint}
                            onChange={this.onElementChange}
                            elementType={this.props.elementType}
                        />
                    </td>
                );
            }
            table.push(<tr key={i}>{children}</tr>);
        }

        return <table><tbody>{table}</tbody></table>;
    }

    render() {
        return (this.createInputTable());
    }

    // Children will call this callback when their input changes.
    // This updates Matrix components data state.
    // Because we can't access child components inner state, we have to use this callback from parent.
    // By doing that we are setting Matrix component as source of thruth.
    private onElementChange = (row: number, col: number, newValue: ValueType) => {
        const copyData = this.state.data.slice();
        copyData[row][col] = newValue;
        this.setState({ data: copyData });
    };
}