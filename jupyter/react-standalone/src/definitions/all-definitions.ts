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
        },

    }
};

export const polyhedron = {
    "name": "Polyhedron",
    "plural": "Polyhedra",
    "attributes": {
        "vertices": "Boolean",
        "rays": "Boolean",
        "lines": "Boolean",
        "inequalities": "Boolean",
        "equations": "Boolean"
    },
    "options": {
        "ambient_dimension": "Integer"
    },
    "raw_types": {
        "hrep": "Boolean",
        "vrep": "Boolean"
    },
    "size": {
        "ambient_dimension": "@options.ambient_dimension",
        "vertices": "Integer",
        "rays": "Integer",
        "lines": "Integer",
        "inequalities": "Integer",
        "equations": "Integer"
    },
    "raw": {
        "hrep": {
            "inequalities": {

                "structure": [2],
                "element": {
                    "type": [
                        {
                            "structure": ["@size.inequalities", "@size.ambient_dimension"],
                            "element": {
                                "type": "Number",
                                "default": "0"
                            }
                        },
                        {
                            "structure": ["@size.inequalities"],
                            "element": {
                                "type": "Number",
                                "default": "0"
                            }
                        }

                    ]
                }
            },
            "equations": {

                "structure": [2],
                "element": {
                    "type": [
                        {
                            "structure": ["@size.inequalities", "@size.ambient_dimension"],
                            "element": {
                                "type": "Number",
                                "default": "0"
                            }
                        },
                        {
                            "structure": ["@size.inequalities"],
                            "element": {
                                "type": "Number",
                                "default": "0"
                            }
                        }

                    ]
                }
            }
        },
        "vrep": {
            "vertices": {
                "structure": ["@size.vertices"],
                "element": {

                    "structure": ["@size.ambient_dimension"],
                    "element":
                        {
                            "type": "Number"
                        }

                }
            },
            "rays": {
                "structure": ["@size.rays"],
                "element": {
                    "structure": ["@size.ambient_dimension"],
                    "element": {
                        "type": "Number"
                    }
                }
            },
            "lines": {
                "structure": ["@size.lines"],
                "element": {
                    "structure": ["@size.ambient_dimension"],
                    "element": {
                        "type": "Number"
                    }
                }
            }
        }
    },
    "features": {
        "bounded": "Boolean",
        "dimension": "Integer"
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
