import _ from 'lodash';
import * as React from "react";
import {graph, polyhedron} from "../definitions/all-definitions";
import {convertToHierarchy} from "../util/helpers";
import {InputGroup} from "./input-group";
import MathObject from "./math-object";

export class GraphForm extends React.Component<any, any> {
    private definition: any;
    private definitionList: any;

    constructor(props: any) {
        super(props);

        this.definition = graph;
        this.definitionList = [graph, polyhedron];
        this.state = {
            selectedDefinition: null,
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
            <div className="container">
                <h1>Math Data Interface - Definition Generation</h1>
                {/*<button onClick={() => {*/}
                    {/*this.setState({*/}
                        {/*selectedDefinition: graph,*/}
                        {/*attributes: {*/}
                            {/*edges: true,*/}
                            {/*vertices: true,*/}
                        {/*},*/}
                        {/*size: {*/}
                            {/*edges: 5,*/}
                            {/*vertices: 5,*/}
                        {/*},*/}
                        {/*options: {*/}
                            {/*'edges.weighted': false,*/}
                        {/*},*/}
                        {/*raw_types: {*/}
                            {/*sparse: true,*/}
                        {/*}*/}
                    {/*})*/}
                {/*}}>*/}
                    {/*Demo Graph Settings*/}
                {/*</button>*/}
                {/*<button onClick={() => {*/}
                    {/*this.setState({*/}
                        {/*selectedDefinition: polyhedron,*/}
                        {/*attributes: {*/}
                            {/*vertices: true,*/}
                            {/*rays: true,*/}
                            {/*lines: true,*/}
                        {/*},*/}
                        {/*size: {*/}
                            {/*vertices: 3,*/}
                            {/*rays: 4,*/}
                            {/*lines: 5,*/}
                            {/*// ambient_dimension: 7*/}
                        {/*},*/}
                        {/*options: {*/}
                            {/*ambient_dimension: 7*/}
                        {/*},*/}
                        {/*raw_types: {*/}
                            {/*vrep: true,*/}
                        {/*}*/}
                    {/*})*/}
                {/*}}>*/}
                    {/*Demo Polyhedron Settings*/}
                {/*</button>*/}

                {/*{this.state.error && this.state.showDataTable && <div>Error!!</div>}*/}

                <div className="border p-2 mb-2 mt-2">
                    Definition:

                    <select onChange={this.changeDefinition}>
                        <option value="none">No Data Type Selected</option>
                        {this.definitionList.map(def => <option key={def.name} value={def.name}>{def.name}</option>)}
                    </select>
                </div>

                {this.renderDefinitionDetails()}
                {this.renderMathObject()}
            </div>
        );
    }

    renderDefinitionDetails() {
        if (this.state.selectedDefinition) {
            // const regex = /@\w+(\.\w+)*/g;
            // const defClone = {...this.state.selectedDefinition};
            // defClone.raw = {};
            // const objString = JSON.stringify(defClone);
            // const result = objString.replace(regex, (match, capture) => {
            //     return _.at(defClone, match.slice(1))[0];
            // });
            // console.log('result', result);
            return (<div>
                <div className="border p-2 mb-2 mt-2">
                    Attributes:
                    <InputGroup items={this.state.selectedDefinition.attributes}
                                onChange={this.createHandler('attributes')}/>
                </div>

                <div className="border p-2 mb-2">
                    Sizes:
                    <InputGroup items={this.state.selectedDefinition.size}
                                dependsOn={this.state.attributes}
                                onChange={this.createHandler('size')}/>
                </div>

                <div className="border p-2 mb-2">
                    Options:
                    <InputGroup items={this.state.selectedDefinition.options}
                                onChange={this.createHandler('options')}
                    />
                </div>

                <div className="border p-2 mb-2">
                    Raw Types:
                    <InputGroup items={this.state.selectedDefinition.raw_types}
                                onChange={this.createHandler('raw_types')}/>
                </div>

                <button className="btn btn-outline-primary" onClick={this.toggleDataTable}>Toggle Data Table</button>
            </div>);
        } else {
            return null;
        }
    }

    renderMathObject() {
        if (this.state.showDataTable && this.checkFormComplete()) {
            return <MathObject
                definition={this.state.selectedDefinition}
                attributes={this.state.attributes}
                size={this.state.size}
                options={convertToHierarchy(this.state.options)}
                raw_types={this.state.raw_types}
                raw={this.state.selectedDefinition.raw}
                onChange={this.onDataChange}/>
        } else {
            return null;
        }
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

    changeDefinition = (event: any) => {
        const val = event.target.value;
        const definition = this.definitionList.find(def => def.name === val);
        if (val == "none") {
            this.setState({selectedDefinition: null});
        } else if (definition !== undefined) {
            this.setState({selectedDefinition: definition});
        }
    }
}
