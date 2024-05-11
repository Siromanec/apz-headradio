import React, { useState } from "react";
import "../css/ChangeSong.css";
import "../css/AddChangeButton.css";
import crossButton from "../data/cross.svg";
import { spotifyClientID, spotifyClientSecret } from "./APIKeys";

async function saveSong(songData) {
  return fetch("http://localhost:8000/modify-music", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(songData),
  }).then((data) => data.json());
}




export default function ChangeSong({profile, APIController, setUserSong}) {
  const [songName, setSongName] = useState();
  const [popUpClass, setPopUpClass] = useState("popup-change");
  function handleClick() {
    setPopUpClass("popup-change show");
  }

  function exitClick() {
    setPopUpClass("popup-change");
  }

  async function handleSongChange(setUserSong) {
    setPopUpClass("popup-change");
    const song = document.getElementById("song-name");
    try {
      const songID = new URL(songName).pathname.split("/").pop();
      const token = await APIController.getToken();
      setUserSong(await APIController.getTrack(token, songID))
    } catch (err) {
      setUserSong("No such song");
    }

    const response = await saveSong({profile, songName})
  }

  return (
    <div className="changeSong">
      <div className={popUpClass}>
        <div className="insert-song">
          <span className="insert-song-desc">Insert song link</span>
          <input
            type="text"
            id="song-id"
            placeholder="Song link . . ."
            onChange={(e) => setSongName(e.target.value)}
          />
          <div className="insert-song-buttons">
            <button className="insert-song-btn" onClick={() => handleSongChange(setUserSong)}>
              Change
            </button>
            <button className="insert-song-btn" onClick={exitClick}>
              Cancel
            </button>
          </div>
        </div>
      </div>
      <div className="lower-button-div">
        <button className="lower-button" onClick={handleClick}>
          Change Song
        </button>
      </div>
    </div>
  );
}
