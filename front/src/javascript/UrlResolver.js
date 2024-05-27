export default class UrlResolver {
    constructor() {
        this.baseUrl = "localhost";
        this.port = 8084;
        this.base = `http://${this.baseUrl}:${this.port}`;
    }

    getMainPageUrl(username, token) {
        return `${this.base}/feed/?username=${username}&token=${token}`;
    }

    getShowUserUrl(username, token) {
        return `${this.base}/show-profile/?username=${username}&token=${token}`;
    }

    getRegisterUserUrl(user, pass, mail) {
        return `${this.base}/register/?user=${user}&password=${pass}&email=${mail}`;
    }

    getSetProfilePhotoUrl(token) {
        return `${this.base}/set-profile-photo/?token=${token}`;
    }

    getLikePostUrl(username, post_id, token) {
        return `${this.base}/like-post/?username=${username}&post_id=${post_id}&token=${token}`;
    }

    getIsLikedPostUrl(username, id, token) {
        return `${this.base}/has-liked/?username=${username}&post_id=${id}&token=${token}`;
    }

    getLoginUrl(user, pass) {
        return `${this.base}/login/?user=${user}&password=${pass}`;
    }

    getNewPostUrl(token) {
        return `${this.base}/new-post/?token=${token}`;
    }

    getModifyMusicUrl(user, music) {
        return `${this.base}/modify-music/?user=${user}&music=${music}&token=${token}`;
    }
}
