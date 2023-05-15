import ProfilePicture from "./profile.jpg";
import spotifyIcon from "./spotify_icon.svg";
import ReactPlayer from "react-player/lazy";
import ReactAudioPlayer from "react-audio-player";
import song from "./staying-alive.mp3";

import PhotoChange from "./PhotoChange";
import React, {useState} from "react";

// const loremIpsumHead = "Lorem ipsum"
// // const loremIpsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
// const loremIpsum = "asdc"
function Posts({ posts }) {
  const listItems = posts.map((post) => (
    <Post text={post.text} header={post.header}></Post>
  ));
  return <div>{listItems}</div>;
}
function Post({ text, header }) {
  return (
    <div>
      <h3>{header}</h3>
      <p>{text}</p>
    </div>
  );
}
function AddContent({ onClick }) {
  return (
    <button onClick={onClick} style={{ width: "50px", height: "50px" }}>
      +
    </button>
  );
}
function Editor() {
  const loremIpsumHead = "Lorem ipsum";
  const loremIpsum =
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
  console.log(loremIpsumHead);
  const [posts, setPosts] = useState(
    Array({ text: loremIpsum, header: loremIpsumHead })
  );
  function handleClick() {
    const nextPosts = posts.slice();
    nextPosts.push({ text: loremIpsum, header: loremIpsumHead });
    setPosts(nextPosts);
  }
  return (
    <div>
      <Posts posts={posts}></Posts>
      <AddContent onClick={handleClick}></AddContent>
    </div>
  );
}
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
  const handlePhoto = () => {setShow(show => true)}
  return (
    <main>
      <section>
        <div className="profilePictureDiv" onClick={handlePhoto}>
          <img src={photo} className="profilePicture" />
          {show ? <PhotoChange onClick={submitHandler}/> : null}
        </div>
        <div className="tag">@beheni</div>
        <div className="status">
          <span>Feeling stable</span>
        </div>
      </section>
      <div className="headRadio" onClick={handleClick}>
        <div>{songName}</div>
        <img src={spotifyIcon} style={{ width: "50px" }}></img>
      </div>
      <section className="recentDiary"></section>
      <section className="textField"></section>
      <Editor></Editor>
    </main>
  );
}
