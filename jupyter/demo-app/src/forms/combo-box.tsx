import * as React from "react";
import {graph} from "../definitions/all-definitions";


export class ComboBox extends React.Component<any, any> {
    constructor(props) {
        super(props);


    }

    handleChange = (e) => {
        this.props.onChange(e);
    };

    render() {
        const types = this.props.choices.map(
            (typeName, index) => <option value={index} key={index}>{typeName}</option>
        );
        return (
            <div>
                <select onChange={this.handleChange}>
                    <option value="-1">Not selected</option>
                    {types}
                </select>
            </div>
        );
    }
}