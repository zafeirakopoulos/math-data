// TODO replace with a service to retrieve all objects

export const graph = {
    name: "Graph",
    plural: "Graphs",
    attributes: ["edges"],
    raw_types: ["dense", "sparse"],
    raw: {
        dense: {
            edges: {
                structure: "Matrix",
                element: ["Boolean", "0"]
            }
        },
        sparse: {
            edges: {
                structure: "List",
                element: {
                    structure: ["Tuple", 2],
                    element: ["Integer", "Integer"]
                }
            }
        }
    }
};

export const graphVertexWeighted = {
    inherits: ["Graph"],
    name: "Vertex Weighted Graph",
    plural: "Vertex Weighted Graphs",
    attributes: ["vertices"],
    parameters: {
        vertex_weight_type: ["Number", "Integer"]
    },
    raw: {
        dense: {
            vertices: {
                structure: "List",
                element: ["{{vertex_weight_type}}", "Integer"]
            }
        },
        sparse: {
            vertices: {
                structure: "List",
                element: ["{{vertex_weight_type}}", "Integer"]
            }
        }
    }
};

export const graphEdgeWeighted = {
    inherits: ["Graph"],
    name: "Edge Weighted Graph",
    parameters: {
        edge_weight_type: ["Number", "Integer"]
    },
    raw: {
        dense: {
            edges: {
                element: ["{{edge_weight_type}}", "Integer"]
            }
        },
        sparse: {
            edges: {
                element: {
                    structure: ["Tuple", 3],
                    element: [
                        ["Integer", "Integer", "{{edge_weight_type}}"],
                        [1, 1, "Integer"]
                    ]
                }
            }
        }
    }
};

export const graphVertexWeightedEdgeWeighted = {
    inherits: ["Vertex Weighted Graph", "Edge Weighted Graph"],
    name: "Vertex and Edge Weighted Graph",
    plural: "Vertex and Edge Weighted Graphs"
};

export class DataDefinitionService {
    defs = {
        "Graph": graph,
        "Vertex Weighted Graph": graphVertexWeighted,
        "Edge Weighted Graph": graphEdgeWeighted,
        "Vertex and Edge Weighted Graph": graphVertexWeightedEdgeWeighted,
    };

    get(name: string) {
        return this.defs[name];
    }
}
