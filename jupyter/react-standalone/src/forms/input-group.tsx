import React, {Component} from 'react';
import {Simulate} from "react-dom/test-utils";
import input = Simulate.input;
import {isObject} from "../util/helpers";

export class InputGroup extends Component<any, any> {
    constructor(props) {
        super(props);
    }

    render() {
        const inputs = [];

        // console.log(this.props);

        for (const key in this.props.items) {
            if (this.props.items.hasOwnProperty(key)) {
                // if the dependsOn for current input is undefined or false, we don't show it. Go to next iteration.
                if (this.props.dependsOn && !this.props.dependsOn[key]) {
                    continue;
                }
                const value = this.props.items[key];
                // console.log('kv', key, value);
                let inputType;
                if (isObject(value)) {
                    inputs.push(
                        <div key={key}>
                            {key}:
                            <InputGroup items={value}
                                        onChange={this.props.onChange}
                                        parentKey={key}/>
                        </div>
                    );
                } else {
                    if (value === "Boolean") {
                        inputType = "checkbox";
                    } else if (value === "integer") {
                        inputType = "text";
                    }

                    const newKey = this.props.parentKey ? (this.props.parentKey + '.' + key) : key;

                    inputs.push(
                        <div key={newKey}>
                            {key}:
                            <input name={newKey}
                                   type={inputType}
                                   onChange={this.props.onChange}/>
                        </div>
                    );
                }


            }
            // checkboxes.push(<input type="checkbox" value={""} onChange={this.props.handleChange}/>);
        }

        return (<div>{inputs}</div>);
    }
}
