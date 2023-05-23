import React, { useState, useEffect } from "react";



export default function AddFriend({ profile, friends}) {
    const [isFriend, setIsFriend] = useState(friends)
    const addHandler = async () => {
            await fetch(`http://localhost:8000/fetch-${!isFriend?"add":"remove"}-friend`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ "username1": profile, "username2": sessionStorage.getItem("username") })
            });
            setIsFriend(!isFriend)
        };
    return <div className="lower-button">
        <button onClick={addHandler}>{!isFriend?"Add Friend":"Remove friend"}</button>
    </div>
}
