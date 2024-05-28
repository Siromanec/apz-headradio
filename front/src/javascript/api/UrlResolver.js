// import ConsulAgent from "./ConsulAgent";

export default class UrlResolver {
    // constructor() {
        // this.consulAgent = new ConsulAgent()
    // }

    resolve() {
        return `http://localhost:8000`;
        // return this.consulAgent.getService("api-gateway")
        // .then(service => {
        //     return `http://${service.host}:${service.port}`
        // })
    }

    getMainPageUrl(username, token) {
        return `${this.resolve()}/feed/?username=${username}&token=${token}`;
    }

    getShowUserUrl(username, token) {
        console.log(username, token);
        return `${this.resolve()}/show-profile/?username=${username}&token=${token}`;
    }

    getRegisterUserUrl(user, pass, mail) {
        return `${this.resolve()}/register/?user=${user}&password=${pass}&email=${mail}`;
    }

    getSetProfilePhotoUrl(token) {
        return `${this.resolve()}/set-profile-photo/?token=${token}`;
    }

    getLikePostUrl(username, post_id, token) {
        return `${this.resolve()}/like-post/?username=${username}&post_id=${post_id}&token=${token}`;
    }

    getIsLikedPostUrl(username, id, token) {
        return `${this.resolve()}/has-liked/?username=${username}&post_id=${id}&token=${token}`;
    }

    getLoginUrl(user, pass) {
        return `${this.resolve()}/login/?user=${user}&password=${pass}`;
    }

    getNewPostUrl(token) {
        return `${this.resolve()}/new-post/?token=${token}`;
    }

    getModifyMusicUrl(user, music, token) {
        return `${this.resolve()}/modify-music/?user=${user}&music=${music}&token=${token}`;
    }

    getAddFriendUrl(usernameFollows, username, token) {
        return `${this.resolve()}/add-friend/?username_follows=${usernameFollows}&username=${username}&token=${token}`;
    }
    getRemoveFriendUrl(usernameFollows, username, token) {
        return `${this.resolve()}/remove-friend/?username_follows=${usernameFollows}&username=${username}&token=${token}`;
    }
    getGetFriendsUrl(username, token) {
        return `${this.resolve()}/get-friends/?username=${username}&token=${token}`;
    }
}
