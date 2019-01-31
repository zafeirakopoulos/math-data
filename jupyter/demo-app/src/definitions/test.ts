interface DataType {
    name: string,
    plural: string,
    attributes: Attribute[]
    raw: RawField[]
}

interface Attribute {
    name: string,
    value: string
}

interface Option {
    name: string,
    value: Option[] | string
}

interface RawField {
    name: string,
    value: RawField | StructureElementPair
}

interface StructureElementPair {
    structure: string[] | number[],
    element: Element | ConditionalStatement
}

interface Element {
    type: string | string[],
    default?: string
}

interface ConditionalStatement {
    if: Condition,
    then: StructureElementPair,
    else?: ConditionalStatement
}

interface Condition {
    variableName: string,
    conditionCheck: boolean
}

type InputType = "Boolean" | "Number" | "Float"

interface Element {
    type: InputType | InputType[],
    default?: string
}
