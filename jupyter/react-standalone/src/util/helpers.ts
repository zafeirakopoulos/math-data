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

// From: https://codereview.stackexchange.com/questions/31831/convert-flat-object-keys-to-hierarchical-one
function eachKeyValue(obj, fun) {
    for (const i in obj) {
        if (obj.hasOwnProperty(i)) {
            fun(i, obj[i]);
        }
    }
}

export function convertToHierarcy(obj) {
    const result = {};
    eachKeyValue(obj, (namespace, value) => {
        const parts = namespace.split(".");
        const last = parts.pop();
        let node = result;
        parts.forEach((key) => {
            node = node[key] = node[key] || {};
        });
        node[last] = value;
    });
    return result;
}

// From: https://gist.github.com/penguinboy/762197
export function flattenObject(ob) {
    const toReturn = {};

    for (const i in ob) {
        if (!ob.hasOwnProperty(i)) { continue; }

        if ((typeof ob[i]) == 'object') {
            const flatObject = flattenObject(ob[i]);
            for (const x in flatObject) {
                if (!flatObject.hasOwnProperty(x)) { continue; }

                toReturn[i + '.' + x] = flatObject[x];
            }
        } else {
            toReturn[i] = ob[i];
        }
    }
    return toReturn;
}

export function countProperties(obj) {
    return Object.keys(obj).length;
}
