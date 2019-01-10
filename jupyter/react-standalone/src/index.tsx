import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {GraphForm} from "./forms/graph-form";
import registerServiceWorker from './registerServiceWorker';
import './style/index.css'

ReactDOM.render(
  <GraphForm />,
  document.getElementById('root') as HTMLElement
);
registerServiceWorker();
