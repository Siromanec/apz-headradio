export default class RequestBodyBuilder {

    static getMainPageRequestBody() {
        return {method: "GET"};
    }

    static getShowUserRequestBody() {
        return {method: "GET"};
    }

    static getRegisterUserRequestBody() {
        return {method: "POST"};
    }

    static getSetProfilePhotoRequestBody({username, image}) {
        return {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({username: username, image: image})
        }
    };

    static getLikePostRequestBody() {
        return {method: "POST"};
    }

    static getIsLikedPostRequestBody() {
        return {method: "POST"};
    }

    static getLoginRequestBody() {
        return {method: "POST"};
    }

    static getNewPostRequestBody({article, username}) {
        return {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                article: article,
                username: username
            }),
        };
    }

    static getModifyMusicRequestBody() {
        return {
            method: "POST",
        };
    }
    static getGetFriendsRequestBody() {
        return {
            method: "GET",
        };
    }
    static getAddFriendRequestBody() {
        return {
            method: "POST",
        };
    }
    static getRemoveFriendRequestBody() {
        return {
            method: "POST",
        };
    }
}
