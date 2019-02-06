import { Widget } from "@phosphor/widgets";

import { Message } from "@phosphor/messaging";
import * as React from "react";
import * as ReactDOM from "react-dom";
// import { GraphForm } from "./forms/graph-form";
import { GraphForm } from "./forms/graph-form";

export class MathDataWidget extends Widget {
    /**
     * Construct a MathData widget.
     */

    /**
     * The main area element associated with the widget.
     */
    public readonly content: HTMLDivElement;
    public readonly textarea: HTMLTextAreaElement;
    public readonly button: HTMLButtonElement;

    constructor() {
        super();

        this.id = "mdb-jupyterlab";
        this.title.label = "MathDataBench";
        this.title.closable = true;

        ReactDOM.render(<GraphForm/>, this.node);
    }

    /**
     * Handle update requests for the widget.
     */
    public onUpdateRequest(msg: Message): void {
        fetch("https://egszlpbmle.execute-api.us-east-1.amazonaws.com/prod")
            .then(response => {
                return response.json();
            })
            .then(data => {
                console.log(data);
            });
    }
}

