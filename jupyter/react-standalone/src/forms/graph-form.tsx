import * as React from "react";
import {graph} from "../definitions/all-definitions";
import {InputGroup} from "./input-group";

export interface IGraphFormState {
    data_type: number,
    raw_type: number,
    input_elements: JSX.Element,
    json_output: object,
    definition: object
}

export class GraphForm extends React.Component<any, any> {
    dataSource = null;

    constructor(props: any) {
        super(props);

        this.state = {
            definition: graph,
            attributes: {},
            options: {},
            raw_types: {},
            sizes: {},
            raw: null
        }

        // console.log(this.state.definition.attributes);
    }

    render() {
        return (
            <div>
                <div className="input-group">
                    Attributes:
                    <InputGroup items={this.state.definition.attributes}
                                onChange={this.createHandler('attributes')}/>
                </div>

                <div className="input-group">
                    Sizes:
                    <InputGroup items={this.state.definition.size}
                                dependsOn={this.state.attributes}
                                onChange={this.createHandler('sizes')}/>
                </div>

                <div className="input-group">
                    Options:
                    <InputGroup items={this.state.definition.options}
                                onChange={this.createHandler('options')}
                    />
                </div>

                <div className="input-group">
                    Raw Types:
                    <InputGroup items={this.state.definition.raw_types}
                                onChange={this.createHandler('raw_types')}/>
                </div>

                <button onClick={() => {console.log(this.state)}}>Generate Form</button>
            </div>
        );
    }

    createHandler = (stateName: string, extraValue?: string) => (event: any) => {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;

        this.setState((prevState) => ({
            [stateName]: {
                ...prevState[stateName],
                [name]: value
            }
        }));
    };
}
