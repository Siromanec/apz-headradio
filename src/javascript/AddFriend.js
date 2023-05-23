import React, { useState, useEffect } from "react";
import "../css/AddChangeButton.css"


export default function AddFriend({ profile, isFriend, setIsFriend, friendsCount, setFriendsCount}) {
    // const [isFriend, setIsFriend] = useState(friends)
    const addHandler = async () => {
            await fetch(`http://localhost:8000/fetch-${!isFriend?"add":"remove"}-friend`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ "username2": profile, "username1": sessionStorage.getItem("username") })
            });
            if(isFriend) {
                setIsFriend(false)
                setFriendsCount(friendsCount - 1)
            }
            else{
                setIsFriend(true)
                setFriendsCount(friendsCount + 1)
            }
            // se
        };
    return <div className="lower-button-div">
        <button className="lower-button" onClick={addHandler}>{!isFriend?"Add Friend":"Remove friend"}</button>
    </div>
}
