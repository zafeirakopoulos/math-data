import merge from "deepmerge";
import {DataDefinitionService} from "../definitions/all-definitions";

export function isArray(a: any) {
    return (!!a) && (a.constructor === Array);
}

export function isObject(a: any) {
    return (!!a) && (a.constructor === Object);
}

export function resolveInheritence(defName: string) {
    const inheritanceNames = resolveInheritenceNames(DataDefinitionService, defName);
    const inheritanceObjects = inheritanceNames.map(name => DataDefinitionService[name]);
    const merged = merge.all(inheritanceObjects);
    return merged;
}

function resolveInheritenceNames(definitions, name) {
    const inherit: string[] = [];
    const def = definitions[name];
    if (def.hasOwnProperty('inherits')) {
        for (const inh of def.inherits) {
            inherit.push(inh);
            inherit.push(resolveInheritenceNames(definitions, inh));
        }
    }

    return flattenDeep(inherit).filter((value, index, arr) => arr.indexOf(value) === index);
}

// From mozilla JS docs: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/flat#reduce_and_concat
function flattenDeep(arr1) {
    return arr1.reduce((acc, val) =>
        Array.isArray(val) ?
            acc.concat(flattenDeep(val)) :
            acc.concat(val), []);
}