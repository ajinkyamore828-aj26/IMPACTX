
export function formatCurrency(amount) {
    return "$" + Number(amount).toFixed(2);
}

export function debounce(fn, delay) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
    };
}
