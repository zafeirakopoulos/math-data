import * as React from "react";
import {graph, DataDefinitionService} from "../definitions/all-definitions";
import {resolveInheritence} from "../util/helpers";
import {SaveJson} from "../util/save-json";
import {ComboBox} from "./combo-box";
import {Matrix} from "./matrix";

export interface IGraphFormState {
    data_type: number,
    raw_type: number,
    input_elements: JSX.Element,
    json_output: object,
    definition: object
}

export class GraphForm extends React.Component<{}, IGraphFormState> {
    constructor(props: any) {
        super(props);

        this.state = {
            data_type: -1,
            raw_type: -1,
            input_elements: null,
            json_output: {},
            definition: {}
        };
    }

    render() {
        return (
            <div>
                Select data type:

                <ComboBox
                    choices={Object.keys(DataDefinitionService)}
                    onChange={this.handleChangeDataType}/>

                Select {graph.name} type:

                <ComboBox
                    choices={graph.raw_types}
                    onChange={this.handleChangeRawType}/>

                {this.createStructure()}

                <SaveJson jsonOutput={this.state.json_output}/>
            </div>
        );
    }

    // = JSX Element Generators = //

    // TODO element must be recursive.
    private createStructure(): JSX.Element {
        if (this.state.raw_type == -1) {
            return null;
        }

        if (typeof this.state.raw_type !== 'undefined') {
            // e.g. "dense" or "sparse", depends on selection.
            const rawTypeName = graph.raw_types[this.state.raw_type];
            if (typeof rawTypeName === 'undefined') {
                return null;
            }

            // raw.dense.edges or raw.sparse.edges
            const attrInfo = graph.raw[rawTypeName][graph.attributes[0]];

            const structureType = attrInfo.structure;
            const elementInfo = attrInfo.element;

            const elementType = elementInfo[0];
            const defaultValue = elementInfo[1];

            const normalizedStructureType = structureType.trim().toLowerCase();
            let col = 0;
            // default 5 row, ultimately row count doesn't matter because we can expand at will.
            let row = 5;
            if (normalizedStructureType === "matrix") {
                // const elemName = elementInfo[0];
                // const elemDefault = elementInfo[1];
                col = 6;
                row = col;
                return (<Matrix row={row}
                                col={col}
                                attrInfo={attrInfo}
                                elementType={elementType}
                                defaultValue={defaultValue}
                                jsonOutputSetter={this.jsonOutputSetter}/>);

            } else if (normalizedStructureType === "list") {
                /* Have error with tuple continer */
                // return (<TupleContainer tup_dimension={2}/>);
                return (<Matrix row={row}
                                col={2}
                                elementType={elementType}
                                defaultValue={defaultValue}
                                jsonOutputSetter={this.jsonOutputSetter}/>)
            }
        }

        return null;
    }

    // = JSON Parsers = //
    private parseAttributes(json) {

    }

    private parseStructure(json) {

    }

    // = Event Handlers = //
    private handleChangeDataType = (event: any) => {
        const dataTypeIndex = event.target.value;
        const definition = resolveInheritence(Object.keys(DataDefinitionService)[dataTypeIndex]);

        this.setState({data_type: dataTypeIndex, definition});
    };

    private handleChangeRawType = (event: any) => {
        this.setState({raw_type: event.target.value});
    };

    private jsonOutputSetter = (json: any) => {
        this.setState({json_output: json});
    };
}