import React, { useState, useEffect } from "react";
import "../css/AddChangeButton.css";

import UrlResolver from "./UrlResolver.js";
const urlResolver = new UrlResolver();

export default function AddFriend({ profile, isFriend, setIsFriend }) {
  const addHandler = async () => {
    await fetch(
      // `http://localhost:8000/${!isFriend ? "add" : "remove"}-friend`,
      urlResolver.getFriendHandlerUrl(),
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username2: sessionStorage.getItem("username"),
          username1: profile,
        }),
      }
    );
    setIsFriend(!isFriend);
  };
  return (
    <div className="lower-button-div">
      <button className="lower-button" onClick={addHandler}>
        {!isFriend ? "Add Friend" : "Remove friend"}
      </button>
    </div>
  );
}
