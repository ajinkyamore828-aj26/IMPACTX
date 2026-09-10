
import { postData } from "./api.js";
import { debounce } from "./utils.js";

export function login(email, password) {
    return postData("/api/login", { email, password });
}

export function logout() {
    console.log("Logged out.");
}
