import React, { useState } from "react";
import "../css/ChangeSong.css";
import "../css/AddChangeButton.css";
import crossButton from "../data/cross.svg";
import { spotifyClientID, spotifyClientSecret } from "./APIKeys";

const APIController = (function () {
  const clientId = spotifyClientID;
  const clientSecret = spotifyClientSecret;

  // private methods
  const _getToken = async () => {
    const result = await fetch("https://accounts.spotify.com/api/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Basic " + btoa(clientId + ":" + clientSecret),
      },
      body: "grant_type=client_credentials",
    });

    const data = await result.json();
    return data.access_token;
  };

  const _getTrack = async (token, songID) => {
    const result = await fetch(`https://api.spotify.com/v1/tracks/${songID}`, {
      method: "GET",
      headers: { Authorization: "Bearer " + token },
    });

    const data = await result.json();
    if (data.name) {
      return data.name + " • " + data.artists[0].name;
    }
    return "No such song";
  };

  return {
    getToken() {
      return _getToken();
    },
    getTrack(token, trackEndPoint) {
      return _getTrack(token, trackEndPoint);
    },
  };
})();

export default function ChangeSong() {
  const [songName, setSongName] = useState();
  const [popUpClass, setPopUpClass] = useState("popup-change");
  function handleClick() {
    setPopUpClass("popup-change show");
  }

  function exitClick() {
    setPopUpClass("popup-change");
  }

  async function handleSongChange() {
    setPopUpClass("popup-change");
    const song = document.getElementById("song-name");
    try {
      const songID = new URL(songName).pathname.split("/").pop();
      const token = await APIController.getToken();
      song.textContent = await APIController.getTrack(token, songID);
    } catch (err) {
      song.textContent = "No such song";
    }
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
            <button className="insert-song-btn" onClick={handleSongChange}>
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
