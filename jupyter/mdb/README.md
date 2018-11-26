# mdb

Adding mdb to Jupyter


## Prerequisites

* JupyterLab

## Installation

```bash
jupyter labextension install mdb
```

## Development

For a development install (requires npm version 4 or later), do the following in the repository directory:

```bash
npm install
npm run build
jupyter labextension link .
```

To rebuild the package and the JupyterLab app:

```bash
npm run build
jupyter lab build
```

Or you can start JupyterLab instance in watch mode so it will keep up with changes

```bash
jupyter lab --watch
```