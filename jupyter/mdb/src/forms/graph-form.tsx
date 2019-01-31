import * as React from "react";
import { graph } from "../definitions/all-definitions";
import { Matrix } from "./matrix";
import { TupleContainer } from "./tuple-container";

export interface IGraphFormState {
    raw_type: string,
    input_elements: JSX.Element,
    json_output: object
}

export class GraphForm extends React.Component<{}, IGraphFormState> {
    constructor(props: any) {
        super(props);

        this.state = {
            raw_type: "",
            input_elements: null,
            json_output: {}
        };
    }

    render() {
        return (
            <div>
                Select {graph.name} types:
                {this.typesComboBox()}
                {this.createStructure()}
                {this.generateJsonSection()}
            </div>
        );
    }

    // = JSX Element Generators = //
    private typesComboBox(): JSX.Element {
        const types = graph.raw_types.map(
            (typeName, index) => <option value={index} key={index}>{typeName}</option>);
        return <select onChange={this.onChangeRawTypeHandler}>
            <option value="-1">Not selected</option>
            {types}
        </select>;
    }

    private generateJsonSection(): JSX.Element {
        return (
            <div>
                <button onClick={this.onGenerateJsonHandler}>Generate JSON</button>
                <textarea value={JSON.stringify(this.state.json_output)}/>
            </div>
        );
    }

    // TODO element must be recursive.
    private createStructure(): JSX.Element {
        if (this.state.raw_type !== "") {
            // @ts-ignore
            const attrInfo = graph.raw[this.state.raw_type][graph.attributes[0]]; // raw.dense.edges or raw.sparse.edges
            const structureType = attrInfo.structure;
            const elementInfo = attrInfo.element;

            const elementType = elementInfo[0];
            const defaultValue = elementInfo[1];

            const normalizedStructureType = structureType.trim().toLowerCase();
            let col = 0;
            let row = 0;
            if (normalizedStructureType === "matrix") {
                // const elemName = elementInfo[0];
                // const elemDefault = elementInfo[1];
                col = 6;
                row = col;
                return (<Matrix row={row} col={col} elementType={elementType} defaultValue={defaultValue}/>);

            } else if (normalizedStructureType === "list") {
                return (<TupleContainer tup_dimension={2}/>);
            }
        } else {
            return null;
        }
    }

    // = Event Handlers = //
    private onChangeRawTypeHandler = (event: any) => {
        this.setState({
            raw_type: graph.raw_types[event.target.value]
        });
    };

    private onGenerateJsonHandler = (event: any) => {

    };
}