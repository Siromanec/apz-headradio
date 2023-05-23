import ProfilePicture from "../data/profile.jpg";
import DefaultProfile from "../data/blank-profile-picture.svg"
import spotifyIcon from "../data/spotify_icon.svg";
import PhotoChange from "./PhotoChange";
import React, { useState, useEffect } from "react";
import EditorWrapper from "./Editor.js";
import PostHeader from "./PostHeader.js";
import Calendar from "react-calendar";
import "../css/Profile.css";
import "../css/Calendar.css";
import { Await, useLoaderData, useParams } from "react-router-dom";
import Post from "./Post.js"


function Posts({ posts, postOrder }) {
  const listItems = postOrder.map((number) => {
    const post = posts.data[number];
    const postWrap = { id: post.idpost, username: post.username, text: post.article, added: post.added, numberLikes: post.nlikes }
    return <Post post={postWrap} images={posts.images[number]}></Post>
  }
  );
  return <>{listItems}</>
}

const formatShortWeekday = (locale, date) => {
  return date.toLocaleDateString(locale, { weekday: "short" }).slice(0, 1);
};



export default function Profile() {
  const [photo, setPhoto] = useState();
  const [show, setShow] = useState(false);
  const [date, setDate] = useState(new Date());
  const { username, posts, friends } = useLoaderData();
  const postOrder = Object.keys(posts.data).sort((a, b) => b - a)
  let currentPost = posts.data[postOrder[0]]
  const songName = "В очах  •  Skryabin";

  const submitHandler = (event) => {
    setPhoto(event.target.files[0])
  };
  console.log(photo);
  const handlePhoto = () => {
    setShow((show) => !show);
  }
  function handleShowFriends() {
    console.log(friends)
  }
  return (
    <main>
      <section className="profileInfo">
        <div className="profileDescription">
          <div className="profilePictureDiv" onClick={handlePhoto}>
            <span className="editText">Change Photo</span>
            <img src={photo??false ?URL.createObjectURL(photo): DefaultProfile} className="profilePicture" />
            <PhotoChange changleHandler={submitHandler} />
          </div>
          <span className="tag">@{username}</span>
        </div>
        <div className="headRadio">
          <div className="Song">
            <img
              className="spotify-icon"
              src={spotifyIcon}
              style={{ width: "40px" }}
            ></img>
            <div className="songName">
              {songName}
            </div>
          </div>
          <div className="Stats">
            <div className="Posts">
              <span>POSTS</span>
              <span className="numbers">{postOrder.length}</span>
            </div>
            <div className="Friends" onClick={handleShowFriends}>
              <span>FRIENDS</span>
              <span className="numbers">{friends.length}</span>
            </div>
          </div>
        </div>
      </section>
      <section className="recentDiary"></section>
      <section className="textField"></section>
      <EditorWrapper></EditorWrapper>
      <Post post={currentPost} /*images={currentPost}*/ headerType="lastPostElement"></Post>
      <div className='calendar-container'>
        <Calendar onChange={setDate}
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
      <Posts posts={posts} postOrder={postOrder.slice(1, postOrder.length)}></Posts>
    </main>
  );
}
