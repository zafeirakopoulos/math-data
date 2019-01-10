import { Widget } from '@phosphor/widgets';

export class MathDataTOC extends Widget {
    /**
     * The elements associated with the widget.
     */
    public readonly content: HTMLDivElement;
    public readonly mathdata: HTMLButtonElement;
    public readonly benhcmarks: HTMLButtonElement;
    public readonly mathdatasearch: HTMLButtonElement;
    public readonly benchmarksearch: HTMLButtonElement;
    public readonly library: HTMLButtonElement;
  
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
  