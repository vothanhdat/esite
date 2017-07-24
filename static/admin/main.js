

function getJquery() {
    return (window.django || {}).jQuery || window.jQuery;
}

Object.defineProperty(window, '$', {
    get: getJquery,
});

