import { IDisposable, DisposableDelegate } from "@phosphor/disposable";

import {
  JupyterLab,
  JupyterLabPlugin,
  ILayoutRestorer
} from "@jupyterlab/application";

import "../style/index.css";

import {
  ICommandPalette,
  InstanceTracker,
  ToolbarButton
} from "@jupyterlab/apputils";

import { JSONExt } from "@phosphor/coreutils";

import { Widget } from "@phosphor/widgets";

import { Message } from "@phosphor/messaging";

import { DocumentRegistry } from "@jupyterlab/docregistry";

import {
  NotebookActions,
  NotebookPanel,
  INotebookModel
} from "@jupyterlab/notebook";

/**
 * An xckd comic viewer.
 */
class MathDataWidget extends Widget {
  /**
   * Construct a MathData widget.
   */
  constructor() {
    super();

    this.id = "mdb-jupyterlab";
    this.title.label = "MathDataBench";
    this.title.closable = true;

    this.addClass("jp-MathDataWidget");

    this.img = document.createElement("img");
    this.img.className = "jp-xkcdCartoon";
    this.node.appendChild(this.img);
    this.img.insertAdjacentHTML(
      "afterend",
      `<div class="jp-xkcdAttribution">
    <a href="https://creativecommons.org/licenses/by-nc/2.5/" class="jp-
    ˓→xkcdAttribution" target="_blank">
    <img src="https://licensebuttons.net/l/by-nc/2.5/80x15.png" />
    </a>
    </div>`
    );
  }
  /**
   * The image element associated with the widget.
   */
  readonly img: HTMLImageElement;
  /**
   * Handle update requests for the widget.
   */
  onUpdateRequest(msg: Message): void {
    fetch("https://egszlpbmle.execute-api.us-east-1.amazonaws.com/prod")
      .then(response => {
        return response.json();
      })
      .then(data => {
        this.img.src = data.img;
        this.img.alt = data.title;
        this.img.title = data.alt;
      });
  }
}

/**
 * Initialization data for the mdb extension.
 */
const extension: JupyterLabPlugin<void> = {
  id: "mdb",
  autoStart: true,
  requires: [ICommandPalette, ILayoutRestorer],
  activate: (
    app: JupyterLab,
    palette: ICommandPalette,
    restorer: ILayoutRestorer
  ) => {
    console.log("JupyterLab extension mdb is activated!");

    let widget: MathDataWidget;
    // Add an application command
    const command: string = "mdb:open";
    app.commands.addCommand(command, {
      label: "MathDataBench",
      execute: () => {
        if (!widget) {
          // Create a new widget if one does not exist
          widget = new MathDataWidget();
          widget.update();
        }
        if (!tracker.has(widget)) {
          // Track the state of the widget for later restoration
          tracker.add(widget);
        }
        if (!widget.isAttached) {
          // Attach the widget to the main work area if it's not there
          app.shell.addToMainArea(widget);
        } else {
          // Refresh the comic in the widget
          widget.update();
        }
        // Activate the widget
        app.shell.activateById(widget.id);
      }
    });

    palette.addItem({ command, category: "MathDataBench" });

    // Track and restore the widget state
    let tracker = new InstanceTracker<Widget>({ namespace: "MathDataBench" });
    restorer.restore(tracker, {
      command,
      args: () => JSONExt.emptyObject,
      name: () => "MathDataBench"
    });
  }
};

/**
 * Activate the extension.
 */
function activate(app: JupyterLab) {
  app.docRegistry.addWidgetExtension("Notebook", new ButtonExtension());
}

export default extension;
