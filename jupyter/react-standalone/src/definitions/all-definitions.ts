// TODO replace with a service to retrieve all objects

// interface IDataType {
//     name: string,
//     plural: string,
//     attributes: any,
//     options: any,
// }

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

export const polynomial = {
    "name": "Polynomial",
    "plural": "Polynomials",
    "attributes": {
        "coefficients": "Boolean",
        "roots": "Boolean"
    },
    "options": {
        "number_variables": "Integer",
        "coefficient_type": {
            "value": "Number",
            "default": "Integer"
        }
    },
    "raw_types": {
        "dense": "Boolean",
        "sparse": "Boolean",
        "roots": "Boolean"
    },
    "size": {
        "variables": "@options.number_variables",
        "degree": {
            "structure": ["@size.variables"],
            "element": {
                "type": "Integer"
            }
        }
    },
    "raw":
        {
            "roots":
                {
                    "roots":
                        {
                            "structure": ["@size.degree"],
                            "element": {
                                "type": "Number"
                            }
                        }
                },
            "dense":
                {
                    "coefficients":
                        {
                            "structure": ["@size.degree"],
                            "element": {
                                "type": "@options.coefficient_type",
                                "default": 0
                            }
                        }
                },
            "sparse":
                {
                    "coefficients":
                        {
                            "structure": ["Integer"],
                            "element":
                                {
                                    "structure": ["2"],
                                    "element":
                                        {
                                            "type": [
                                                "Number",
                                                {
                                                    "structure": ["@size.variables"],
                                                    "element": {
                                                        "type": "Integer"
                                                    }
                                                }
                                            ]
                                        }
                                }
                        }
                }
        },
    "features": {
        "number of terms": {
            "value": "Integer",
            "default": "infinity"
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
