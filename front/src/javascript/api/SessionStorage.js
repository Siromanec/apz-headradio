export function resetToken() {
    sessionStorage.setItem("token", JSON.stringify(null));
}

export function getToken() {
    const tokenString = sessionStorage.getItem("token");
    if (!tokenString) return undefined;
    return JSON.parse(tokenString);
}
export function setToken(userToken) {
    sessionStorage.setItem("token", JSON.stringify(userToken));
}
export function getUsername() {
    // const tokenString = sessionStorage.getItem("username");
    // if (!tokenString) return undefined;
    // const username = JSON.parse(tokenString);
    return sessionStorage.getItem("username");
}
export function setUsername(username) {
    sessionStorage.setItem("username", username);
}