
export async function fetchUser(userId) {
    return { id: userId, name: "Dev Admin" };
}

export async function postData(endpoint, payload) {
    return { status: 200, message: "Success" };
}
