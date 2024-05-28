export function resetToken() {
    sessionStorage.setItem("token", JSON.stringify(null));
}

export function getToken() {
    const tokenString = sessionStorage.getItem("token");
    if (!tokenString) return undefined;
    const userToken = JSON.parse(tokenString);
    return userToken?.token;
}
export function setToken(userToken) {
    sessionStorage.setItem("token", JSON.stringify(userToken));
}
