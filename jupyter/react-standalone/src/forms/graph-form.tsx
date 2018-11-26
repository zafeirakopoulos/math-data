import * as React from "react";
import {graph} from "../definitions/all-definitions";
import {InputGroup} from "./input-group";
import {InputGroupDetailed} from "./input-group-detailed";

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
                                enable={this.state.attributes}
                                onChange={this.createHandler('sizes')}/>
                </div>

                <div className="input-group">
                    Attribute Details:
                    <InputGroup items={this.state.definition.options}
                                onChange={this.createHandler('options')}
                    />
                    {/*<InputGroupDetailed*/}
                        {/*items={this.state.definition.attributes}*/}
                        {/*enable={this.state.attributes}*/}
                        {/*onChange={this.createHandler('sizes')}/>*/}
                </div>
            </div>
        );
    }

    createHandler = (stateName: string, extraValue?: object) => (event: any) => {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;

        this.setState((prevState) => ({
            [stateName]: {
                ...prevState[stateName],
                [name]: value
            }
        }));
    }
}