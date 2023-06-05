import React, { useState, useEffect } from "react";
import "../css/AddChangeButton.css";

export default function AddFriend({ profile, isFriend, setIsFriend }) {
  const addHandler = async () => {
    await fetch(
      `http://localhost:8000/fetch-${!isFriend ? "add" : "remove"}-friend`,
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
