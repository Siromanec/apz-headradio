import ProfilePicture from "../data/profile.jpg";
import spotifyIcon from "../data/spotify_icon.svg";
import ReactPlayer from "react-player/lazy";
import ReactAudioPlayer from "react-audio-player";
import song from "../data/staying-alive.mp3";
import PhotoChange from "./PhotoChange";
import React, { useState, useEffect } from "react";
import EditorWrapper from "./Editor.js";
import PostHeader from "./PostHeader.js";
import Calendar from "react-calendar";
import "../css/Profile.css";
import "../css/Calendar.css";
import { Await, useLoaderData, useParams } from "react-router-dom";
// const loremIpsumHead = "Lorem ipsum"
// // const loremIpsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
// const loremIpsum = "asdc"

async function getUserPosts(username) {}
function getSavedUserName() {
  return sessionStorage.getItem("username");
}
// function Posts({ posts }) {
//   const listItems = posts.map((post) => (
//     <Post text={post.text} header={post.header}></Post>
//   ));
//   return <div>{listItems}</div>;
// }
// function Post({ text, header }) {
//   return (
//     <div className="post">
//       <h3>{header}</h3>
//       <p>{text}</p>
//     </div>
//   );
// }
const formatShortWeekday = (locale, date) => {
  return date.toLocaleDateString(locale, { weekday: "short" }).slice(0, 1);
};

export default function Profile() {
  const [photo, setPhoto] = useState(ProfilePicture);
  const [show, setShow] = useState(false);
  const [date, setDate] = useState(new Date());
  const {username, posts, friends} = useLoaderData();
  const postOrder = Object.keys(posts.data).sort((a, b) => b-a)
  // const [userPosts, setUserPosts] = useState(new Date());
  let currentPost = postOrder[-1]
  const songName = "В очах  •  Skryabin";

//  const { username } = useParams()

  const submitHandler = (file) => {
    const formData = new FormData();
    formData.append("File", photo);
    fetch(
      "https://freeimage.host/api/1/upload?key=6d207e02198a847aa98d0a2a901485a5",
      { method: "POST", body: formData, mode: "no-cors" }
    )
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
      });
  };
  const handleClick = () => {
    window.location.replace(
      "https://open.spotify.com/track/6yLOGWTvvVXyPBEJUkaFZG?si=6666fde48d6947a1"
    );
  };
  const handlePhoto = () => {
    setShow((show) => !show);
  };
  // console.log(posts);
  console.log(Object.keys(posts.data).sort((a, b) => b-a))
  
  // posts.then(console.log(posts))
  // getUserPosts("user");

  // pop first, show other
  return (
    <main>
      <section className="profileInfo">
        <div className="profileDescription">
          <div className="profilePictureDiv" onClick={handlePhoto}>
            <span className="editText">Change Photo</span>
            <img src={photo} className="profilePicture" />
            {show ? <PhotoChange onClick={submitHandler} /> : null}
          </div>
          <span className="tag">@beheni</span>
        </div>
        <div className="headRadio">
          <div className="Song">
            <img
              className="spotify-icon"
              src={spotifyIcon}
              style={{ width: "40px" }}
              onClick={handleClick}
            ></img>
            <div className="songName" onClick={handleClick}>
              {songName}
            </div>
          </div>
          <div className="Stats">
            <div className="Posts">
              <span>POSTS</span>
              <span className="numbers">23</span>
            </div>
            <div className="Friends">
              <span>FRIENDS</span>
              <span className="numbers">10</span>
            </div>
          </div>
        </div>
      </section>
      <section className="recentDiary"></section>
      <section className="textField"></section>
      <EditorWrapper></EditorWrapper>
      <PostHeader
        headerType="lastPostElement"
        nickName="Beheni"
        avatar={ProfilePicture}
      ></PostHeader>
      <div className="calendar-container">
        <Calendar
          onChange={setDate}
          value={date}
          maxDetail="month"
          showDoubleView
          locale="en"
          minDetail="month"
          tileClassName={({ date, view }) => {
            // console.log(date)
            // console.log(date.toDateString())
            if (
              date.getDay() === 21 &&
              date.getMonth() === 5 &&
              date.getFullYear() === 2023
            ) {
              return "low";
            }
            // if(date.format("DD-MM-YYYY").toDateString()===("21-05-2023")){
            //  return  'low'
            // }
          }}
          formatShortWeekday={formatShortWeekday}
        />
      </div>
      <p className="text-center">
        <span className="bold">Selected Date:</span> {date.toDateString()}
      </p>
    </main>
  );
}
