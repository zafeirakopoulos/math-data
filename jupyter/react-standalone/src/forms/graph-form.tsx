import * as React from "react";
import {graph, polyhedron} from "../definitions/all-definitions";
import {convertToHierarcy} from "../util/helpers";
import {InputGroup} from "./input-group";
import MathObject from "./math-object";

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
            size: {},
            showDataTable: false,
            data: [],
        }

        // console.log(this.state.definition.attributes);
    }

    render() {
        const {
            attributes,
            options,
            raw_types,
            size,
            raw,
        } = this.state;

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
                                onChange={this.createHandler('size')}/>
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

                <button onClick={this.toggleDataTable}>Toggle Data Table</button>

                {
                    this.state.showDataTable &&
                    <MathObject attributes={attributes}
                                size={size}
                                options={convertToHierarcy(options)}
                                raw_types={raw_types}
                                raw={this.state.definition.raw}
                                onChange={this.onDataChange}/>
                }
            </div>
        );
    }

    toggleDataTable = (event: any) => {
        this.setState({
            showDataTable: !this.state.showDataTable
        })
    };

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

    onDataChange = (row, col) => (event: any) => {
        const target = event.target;
        const value = target.value;

        console.log('rc', row, col);

        const index = this.state.data.indexOf(val => val.row === row && val.col === col);
        if (index >= 0) {
            const copy = this.state.data[index];
            copy.value = value;
            this.setState({
                data: copy
            })
        } else {
            this.setState({
                data: this.state.data.concat({'row': row, 'col': col, 'value': value})
            })
        }
        console.log('onDataChange', event);
    };
}
