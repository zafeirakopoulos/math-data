export function isArray(a: any) {
    return (!!a) && (a.constructor === Array);
};

export function isObject(a: any) {
    return (!!a) && (a.constructor === Object);
}
