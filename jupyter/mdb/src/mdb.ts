import { Widget } from "@phosphor/widgets";

import { Message } from "@phosphor/messaging";

export class MathDataWidget extends Widget {
  /**
   * Construct a MathData widget.
   */

  /**
   * The main area element associated with the widget.
   */
  readonly content: HTMLDivElement;
  readonly textarea: HTMLTextAreaElement;
  readonly button: HTMLButtonElement;

  constructor() {
    super();

    this.id = "mdb-jupyterlab";
    this.title.label = "MathDataBench";
    this.title.closable = true;

    this.addClass("jp-MathDataWidget");

    this.content = document.createElement("div");

    this.textarea = document.createElement("textarea");
    this.textarea.cols = 40;
    this.textarea.placeholder = "Here you enter the text";
    this.content.appendChild(this.textarea);

    this.button = document.createElement("button");
    this.button.innerHTML = "MDB submit";
    this.button.style.height = "30px";
    this.button.style.width = "100px";
    this.content.appendChild(this.button);

    this.node.appendChild(this.content);
  }

  /**
   * Handle update requests for the widget.
   */
  onUpdateRequest(msg: Message): void {
    fetch("https://egszlpbmle.execute-api.us-east-1.amazonaws.com/prod")
      .then(response => {
        return response.json();
      })
      .then(data => {
        console.log(data);
      });
  }
}

export class MathDataTOC extends Widget {
  /**
   * The elements associated with the widget.
   */
  readonly content: HTMLDivElement;
  readonly mathdata: HTMLButtonElement;
  readonly benhcmarks: HTMLButtonElement;
  readonly mathdatasearch: HTMLButtonElement;
  readonly benchmarksearch: HTMLButtonElement;
  readonly library: HTMLButtonElement;

  /**
   * Construct a MathData widget.
   */
  constructor() {
    super();

    this.id = "mdb-toc";
    this.title.label = "MathDataBench";
    this.title.closable = true;
    this.addClass("MathDataTOC");

    this.content = document.createElement("div");

    this.mathdata = document.createElement("button");
    this.mathdata.innerHTML = "Math Data";
    this.mathdata.classList.add("toc-button");
    this.content.appendChild(this.mathdata);

    this.benhcmarks = document.createElement("button");
    this.benhcmarks.innerHTML = "Becnhmarks";
    this.benhcmarks.classList.add("toc-button");
    this.content.appendChild(this.benhcmarks);

    this.mathdatasearch = document.createElement("button");
    this.mathdatasearch.innerHTML = "Math Data Search";
    this.mathdatasearch.classList.add("toc-button");
    this.content.appendChild(this.mathdatasearch);

    this.benchmarksearch = document.createElement("button");
    this.benchmarksearch.innerHTML = "Becnhmarks Search";
    this.benchmarksearch.classList.add("toc-button");
    this.content.appendChild(this.benchmarksearch);

    this.library = document.createElement("button");
    this.library.innerHTML = "Library";
    this.library.classList.add("toc-button");
    this.content.appendChild(this.library);

    this.node.appendChild(this.content);
  }
}
