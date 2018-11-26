/**
 * Generic text input element.
 * Currently used by only matrix component
 */
import * as React from "react";
import { ValueType } from "../definitions/types";

interface IInputElementProps {
    elementType: string,
    value: ValueType,
    onChange: (row: number, col: number, newVal: any) => void,
    row: number,
    col: number,
}

interface IInputElementState {
    valid: boolean
}

// Usage: <InputElement elementType=boolean|number|... value=value />
export class InputElement extends React.Component<any, IInputElementState> {
    constructor(props: IInputElementProps) {
        super(props);
        this.state = {
            valid: true
        };
    }

    render() {
        return (<input type="text"
                       pattern="[0-9]*"
                       value={this.props.value}
                       onChange={this.onChange}
                       className="matrixInput"
        />);
    }

    private onChange = (event: any) => {
        console.log('row: ', this.props.row, 'col: ', this.props.col, 'value: ', event.target.value);
        this.props.onChange(this.props.row, this.props.col, event.target.value);
    };
}