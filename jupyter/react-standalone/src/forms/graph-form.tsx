import _ from 'lodash';
import * as React from "react";
import {graph, polyhedron} from "../definitions/all-definitions";
import {convertToHierarchy} from "../util/helpers";
import {InputGroup} from "./input-group";
import MathObject from "./math-object";

export class GraphForm extends React.Component<any, any> {
    private definition: any;

    constructor(props: any) {
        super(props);
        this.definition = graph;
        this.state = {
            attributes: {},
            options: {},
            raw_types: {},
            size: {},
            showDataTable: false,
            data: [],
        }

        // console.log(this.definition.attributes);
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
                <button onClick={() => {
                    this.setState({
                        attributes: {
                            edges: true,
                            vertices: true,
                        },
                        size: {
                            edges: 5,
                            vertices: 5,
                        },
                        options: {
                            'edges.weighted': true,
                        },
                        raw_types: {
                            dense: true,
                        }
                    })
                }}>
                    Demo Settings
                </button>
                {this.state.error && this.state.showDataTable && <div>Error!!</div>}
                <div className="input-group">
                    Attributes:
                    <InputGroup items={this.definition.attributes}
                                onChange={this.createHandler('attributes')}/>
                </div>

                <div className="input-group">
                    Sizes:
                    <InputGroup items={this.definition.size}
                                dependsOn={this.state.attributes}
                                onChange={this.createHandler('size')}/>
                </div>

                <div className="input-group">
                    Options:
                    <InputGroup items={this.definition.options}
                                onChange={this.createHandler('options')}
                    />
                </div>

                <div className="input-group">
                    Raw Types:
                    <InputGroup items={this.definition.raw_types}
                                onChange={this.createHandler('raw_types')}/>
                </div>

                <button onClick={this.toggleDataTable}>Toggle Data Table</button>

                {
                    this.state.showDataTable &&
                    this.checkFormComplete() &&
                    <MathObject
                        definition={this.definition}
                        attributes={attributes}
                        size={size}
                        options={convertToHierarchy(options)}
                        raw_types={raw_types}
                        raw={this.definition.raw}
                        onChange={this.onDataChange}/>
                }
            </div>
        );
    }

    toggleDataTable = (event: any) => {
        this.setState({
            showDataTable: !this.state.showDataTable,
            complete: this.checkFormComplete()
        })
    };

    checkFormComplete() {
        if (!_.isEmpty(this.state.attributes) && !_.isEmpty(this.state.size) && !_.isEmpty(this.state.options) && !_.isEmpty(this.state.raw_types)) {
            return true;
        } else {
            return false;
        }
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
