import blankProfilePicture from "./blank-profile-picture.svg";
import spotifyIcon from "./spotify_icon.svg";
import ReactPlayer from "react-player/lazy";
import ReactAudioPlayer from "react-audio-player";
import song from "./staying-alive.mp3";
import { useState } from "react";

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
  const songName = "Staying Alive";
  return (
    <main>
      <section>
        <div className="profilePictureDiv">
          <img src={blankProfilePicture} className="profilePicture" />
        </div>
        <div className="status">
          <span>Feeling perky</span>
        </div>
      </section>
      <section className="headRadio">
        <div>{songName}</div>
        <img src={spotifyIcon} style={{ width: "50px" }}></img>
        <ReactAudioPlayer src={song} controls />
      </section>
      <section className="recentDiary"></section>
      <section className="textField"></section>
      <Editor></Editor>
    </main>
  );
}
