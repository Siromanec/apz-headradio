export default class UrlResolver {
  constructor() {
    this.baseUrl = "localhost";
    this.port = 8084;
    this.base = `http://${this.baseUrl}:${this.port}`;
  }
  getMainPageUrl(username) {    
    return `${this.base}/main-page/?username=${username}`;
  }

  getShowUserUrl(username) {
    return `${this.base}/show-user/?username=${username}`;
  }

  getRegisterUserUrl(user, pass, mail) {
    return `${this.base}/register/?user=${user}&passw=${pass}&mail=${mail}`;
  }

  getModifyProfilePhotoUrl() {
    return `${this.base}/modify-profile-photo`;
  }

  getLikePostUrl(username, post_id) {
    return `${this.base}/like-post/?username=${username}&post_id=${post_id}`;
  }

  getIfLikedPostUrl(username, id) {
    return `${this.base}/has-liked/?username=${username}&post_id=${id}`;
  }

  getLoginUrl(user, pass) {
    return `${this.base}/login/?user=${user}&passw=${pass}`;
  }

  getNewPostUrl() {
    return `${this.base}/new-post`;
  }

  getModifyMusicUrl(user, music) {
    return `${this.base}/modify-music/?user=${user}&music=${music}`;
  }
}
