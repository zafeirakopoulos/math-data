export const graph = {
    "name": "Graph",
    "plural": "Graphs",
    "attributes": {
        "edges": "Boolean",
        "vertices": "Boolean"
    },
    "options": {
        "edges": {
            "weighted": "Boolean",
            "directed": "Boolean"
        },
        "vertices": {
            "weighted": "Boolean"
        }
    },
    "raw_types": {
        "dense": "Boolean",
        "sparse": "Boolean"
    },
    "size": {
        "edges": "integer",
        "vertices": "integer"
    },
    "raw": {
        "dense": {
            "edges": {
                "structure": ["@size.vertices", "@size.vertices"],
                "element": {
                    "type": "Number",
                    "default": "0"
                }
            },
            "vertices": {
                "structure": ["@size.vertices"],
                "element": {
                    "type": "Number",
                    "default": "0"
                }
            }
        },
        "sparse": {
            "edges": {
                "structure": ["@size.edges"],
                "element": {
                    "if": {
                        "@options.edges.weighted": true
                    },
                    "then": {
                        "structure": [3],
                        "element":
                            {
                                "type": ["Integer", "Integer", "Number"]
                            }
                    },
                    "else": {
                        "if": {
                            "@options.edges.weighted": false
                        },
                        "then": {
                            "structure": [2],
                            "element":
                                {
                                    "type": ["Integer", "Integer"]
                                }
                        }
                    }
                }
            },
            "vertices": {
                "structure": ["@size.vertices"],
                "element": {
                    "type": "Number",
                    "default": "0"
                }
            }
        }
    }
};

export class DataDefinitionService {
    static defs = {
        "Graph": graph,
    };

    static get(name: string) {
        return this.defs[name];
    }
}
