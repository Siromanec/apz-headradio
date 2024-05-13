class UrlResolver {
  constructor() {
    this.baseUrl = "localhost";
    this.port = 9000;
    this.base = `http://${this.baseUrl}:${this.port}`;
  }
  getMainPageUrl(username) {    
    return `${this.base}/main-page?${username}`;
  }

  getShowUserUrl(username) {
    return `${this.base}/show-user?${username}`;
  }

  getRegisterUserUrl(user, pass, mail) {
    return `${this.base}/register?${user}&${pass}&${mail}`;
  }

  getModifyProfilePhotoUrl(user) {
    return `${this.base}/modify-profile-photo?${user}`;
  }

  getLikePostUrl(username, post_id) {
    return `${this.base}/like-post?${username}&${post_id}`;
  }

  getIfLikedPostUrl(username, id) {
    return `${this.base}/?${username}&${id}`;
  }

  getLoginUrl(user, pass) {
    return `${this.base}/login?${user}&${pass}`;
  }

  getNewPostUrl() {
    return `${this.base}/new-post`;
  }

  getModifyMusicUrl() {
    return `${this.base}/modify-music`;
  }
}
