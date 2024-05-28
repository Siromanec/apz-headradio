import React, {useState, useEffect} from "react";
import "../css/AddChangeButton.css";

import UrlResolver from "./api/UrlResolver.js";
import RequestBodyBuilder from "./api/RequestBodyBuilder";
import {getToken, setToken, resetToken} from "./api/Token";

const urlResolver = new UrlResolver();

export default function AddFriend({profile, isFriend, setIsFriend}) {
    const addHandler = async () => {
        await fetch(
            urlResolver.getAddFriendUrl(
                sessionStorage.getItem("username"),
                profile,
                getToken(),
            ),
            RequestBodyBuilder.getAddFriendRequestBody()
        );
        setIsFriend(true);
    }
    const removeHandler = async () => {
        await fetch(
            urlResolver.getRemoveFriendUrl(
                sessionStorage.getItem("username"),
                profile,
                getToken(),
            ),
            RequestBodyBuilder.getRemoveFriendRequestBody()
        );
        setIsFriend(false);
    };

    return (
        <div className="lower-button-div">
            <button className="lower-button" onClick={!isFriend ? addHandler : removeHandler}>
                {!isFriend ? "Add Friend" : "Remove friend"}
            </button>
        </div>
    );
}
