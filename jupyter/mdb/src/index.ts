// Copyright (c) MathDataBench Development Team.

import {
  JupyterLab,
  JupyterLabPlugin,
  ILayoutRestorer
} from "@jupyterlab/application";

import "../style/index.css";

import { ICommandPalette, InstanceTracker } from "@jupyterlab/apputils";

import { Widget } from "@phosphor/widgets";

import {
  JSONExt //Token
} from "@phosphor/coreutils";

import { MathDataWidget, MathDataTOC } from "./mdb";

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

    const { commands } = app;

    let widget: MathDataWidget;

    // Add an application command
    const command: string = "mdb:open";
    commands.addCommand(command, {
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

    let tocwidget: MathDataTOC;
    tocwidget = new MathDataTOC();

    app.shell.addToLeftArea(tocwidget, { rank: 700 });
  }
};

export default extension;
