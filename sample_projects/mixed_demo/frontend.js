
async function loadStatus() {
    const res = await fetch("/api/status");
    return res.json();
}
