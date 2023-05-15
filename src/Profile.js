import ProfilePicture from "./profile.jpg";
import spotifyIcon from "./spotify_icon.svg";
import ReactPlayer from "react-player/lazy";
import ReactAudioPlayer from "react-audio-player";
import song from "./staying-alive.mp3";
import "./Profile.css"
import PhotoChange from "./PhotoChange";
import React, {useState} from "react";

export default function Profile() {
  
  const [photo, setPhoto] = useState(ProfilePicture)
  const [show, setShow] = useState(false)
  const songName = "Skryabin - В очах"
  const submitHandler = (file) => {
      const formData = new FormData();
		  formData.append('File', photo);
      fetch('https://freeimage.host/api/1/upload?key=6d207e02198a847aa98d0a2a901485a5', {method: "POST", body: formData, mode: 'no-cors'}).then((response)=>response.json()).then((result)=>{console.log(result)})
  }
  const handleClick = () => {window.location.replace("https://open.spotify.com/track/6yLOGWTvvVXyPBEJUkaFZG?si=6666fde48d6947a1")}
  const handlePhoto = () => {setShow(show => !show)}
  return (
    <main>
      <section className="profileInfo">
        <div className="profilePictureDiv" onClick={handlePhoto}>
          <img src={photo} className="profilePicture" />
          {show ? <PhotoChange onClick={submitHandler}/> : null}
        <div className="tag">@beheni</div>
        <div className="status">
          <span>Feeling stable</span>
        </div>
        </div>
      <div className="headRadio" onClick={handleClick}>
        <div className="Song">
          <img src={spotifyIcon} style={{ width: "50px" }}></img>
          <div>{songName}</div>
        </div>
        <div className="Stats">
          <div className="Posts">
            <p>Posts</p>
            <p>23</p>
          </div>
          <div className="Friends">
            <p>Friends</p>
            <p>10</p>
          </div>
          </div>
        </div>
      </section>
      <section className="recentDiary"></section>
    </main>
  );
}
