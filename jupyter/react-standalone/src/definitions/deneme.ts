const x = {
    "attributes": [
        "vertices",
        "edges"
    ],
    "parameters": {
        "vertex_weight_type": [
            "Number",
            "Integer"
        ],
        "edge_weight_type": [
            "Number",
            "Integer"
        ]
    },
    "raw": {
        "dense": {
            "vertices": {
                "structure": "List",
                "element": [
                    "{{vertex_weight_type}}",
                    "Integer"
                ]
            },
            "edges": {
                "structure": "Matrix",
                "element": [
                    "Boolean",
                    "0",
                    "{{edge_weight_type}}",
                    "Integer"
                ]
            }
        },
        "sparse": {
            "vertices": {
                "structure": "List",
                "element": [
                    "{{vertex_weight_type}}",
                    "Integer"
                ]
            },
            "edges": {
                "structure": "List",
                "element": {
                    "structure": [
                        "Tuple",
                        2,
                        "Tuple",
                        3
                    ],
                    "element": [
                        "Integer",
                        "Integer",
                        [
                            "Integer",
                            "Integer",
                            "{{edge_weight_type}}"
                        ],
                        [
                            1,
                            1,
                            "Integer"
                        ]
                    ]
                }
            }
        }
    },
    "raw_types": [
        "dense",
        "sparse"
    ]
}

const y = {
    "raw": {
        "dense": {
            "edges": [[1, 2, 1.1], [1, 3, 2.0], [1, 4, 3.1], [2, 3, 0.5], [2, 4, 7.2], [3, 4, 2.2], [3, 5, 3.2], [4, 5, 3.3]],
            "vertices": [1, 2, 3, 4, 5]
        }
    },
    "attributes": ["edges", "vertices"],
    "plural": "Graphs",
    "name": "Graph",
    "raw_types": ["dense"],
    "type": "Vertex and Edge Weighted Graph",
    "parameters": {"vertex_weight_type": ["Integer"], "edge_weight_type": ["Number"]}
};