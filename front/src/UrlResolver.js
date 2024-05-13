class UrlResolver {
  constructor() {
    this.baseUrl = "localhost";
    this.port = 9000;
    this.base = `http://${this.baseUrl}:${this.port}`;
  }
  getMainPageUrl() {    
    return `${this.base}/main-page`;
  }

  getShowUserUrl(username) {
    return `${this.base}/show-user?${username}`;
  }

  getRegisterUserUrl(user, pass, mail) {
    return `${this.base}/register?${user}&${pass}&${mail}`;
  }
}
