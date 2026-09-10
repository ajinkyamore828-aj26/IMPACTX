
import { login, logout } from "./auth.js";
import { fetchUser } from "./api.js";
import { debounce } from "./utils.js";

async function initApp() {
    console.log("Initializing Web App...");
    const user = await fetchUser("usr_101");
    if (user) {
        login("user@test.com", "token");
    }
}

initApp();
