import DefaultProfile from "../data/blank-profile-picture.svg";
import spotifyIcon from "../data/spotify_icon.svg";
import PhotoChange from "./PhotoChange";
import React, { useState, useEffect } from "react";
import EditorWrapper from "./Editor.js";
import PostHeader from "./PostHeader.js";
import Calendar from "react-calendar";
import "../css/Profile.css";
import "../css/Calendar.css";
import { Await, useLoaderData, useParams } from "react-router-dom";
import Post from "./Post.js";
import ChangeSong from "./ChangeSong";
import AddFriend from "./AddFriend";

export function Posts({ posts, postOrder }) {
  const listItems = postOrder.map((number) => {
    const post = posts.data[number];
    if (post) {
      const postWrap = {
        id: post.idpost,
        username: post.username,
        text: post.article,
        added: post.added,
        numberLikes: post.nlikes,
      };
      return <Post post={postWrap} images={posts.images[number]}></Post>;
    }
  });
  return <>{listItems}</>;
}

const formatShortWeekday = (locale, date) => {
  return date.toLocaleDateString(locale, { weekday: "short" }).slice(0, 1);
};

export default function Profile() {
  const { username, avatar, posts, friends } = useLoaderData();
  
  const [isCurrentUser, setIsCurrentUser] = useState(
    username === sessionStorage.getItem("username")
  );
  const [isFriend, setIsFriend] = useState(
    !isCurrentUser && friends.includes(sessionStorage.getItem("username"))
  );

  const [photo, setPhoto] = useState(avatar);
  const [show, setShow] = useState(false);
  const [date, setDate] = useState(new Date());
  const [friendsCount, setFriendsCount] = useState(friends.length);
  
  const postOrder = Object.keys(posts.data).sort((a, b) => b - a);
  let currentPost = posts.data[postOrder[0]];

  const submitHandler = async (event) => {
    const file = URL.createObjectURL(event.target.files[0]);
    setPhoto(file);
    const body = {
      username: sessionStorage.getItem("username"),
      picture: file,
    };
    return await fetch("http://localhost:8000/fetch-modify-profile-photo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
  };

  const handlePhoto = () => {
    setShow((show) => !show);
  };
  function handleShowFriends() {
    console.log(friends);
  }
  useEffect(() => {
    setIsCurrentUser(username === sessionStorage.getItem("username"))
    setPhoto(avatar)
    setFriendsCount(friends.length)
  }, [username])
  // useEffect(() => {
  //   setIsCurrentUser(username === sessionStorage.getItem("username"))
  //   setPhoto(avatar)
  //   setFriendsCount(friends.length)
  // }, [friendsCount])
  // useEffect(() => {
  //   // setIsCurrentUser(username === sessionStorage.getItem("username"))
  // }, [friends])
  return (
    <main>
      <section className="profileInfo">
        <div className="profileDescription">
          <div className={`profilePictureDiv ${isCurrentUser ? "can-change-picture":""}`}>
            <span className="editText" onClick={handlePhoto}>Change Photo</span>
            <img src={photo ? photo : DefaultProfile} className="profilePicture" />
            {show ? <PhotoChange isSessionUser={isCurrentUser}/> : null}
          </div>
          <span className="tag">@{username}</span>
        </div>
        <div className="ProfileInfoAside">
          <div className="headRadio">
            <div className="Song">
              <img
                className="spotify-icon"
                src={spotifyIcon}
                style={{ width: "40px" }}
                onClick={handleSongClick}
              ></img>
              <span id="song-name" className="songName" onClick={handleSongClick}>No added song</span>
            </div>
            <div className="Stats">
              <div className="Posts">
                <span>POSTS</span>
                <span className="numbers">{postOrder.length}</span>
              </div>
              <div className="Friends" onClick={handleShowFriends}>
                <span>FRIENDS</span>
                <span className="numbers">{friendsCount}</span>
              </div>
            </div>
          </div>
          {isCurrentUser ? (
            <ChangeSong />
          ) : (
            <AddFriend profile={username} isFriend={isFriend}  friendsCount={friendsCount} setIsFriend={setIsFriend} setFriendsCount={setFriendsCount}/>
          )}
        </div>
      </section>
      <section className="recentDiary"></section>
      <section className="textField"></section>
      <EditorWrapper></EditorWrapper>
      <Post
        post={currentPost ?? false ? currentPost : {}}
        /*images={currentPost}*/ headerType="lastPostElement"
      ></Post>
      <div className="calendar-container">
        <Calendar
          onChange={setDate}
          value={date}
          maxDetail="month"
          showDoubleView
          locale="en"
          minDetail="month"
          tileClassName={({ date, view }) => {
            if (
              date.getDay() === 21 &&
              date.getMonth() === 5 &&
              date.getFullYear() === 2023
            ) {
              return "low";
            }
          }}
          formatShortWeekday={formatShortWeekday}
        />
      </div>
      <p className="text-center">
        <span className="bold">Selected Date:</span> {date.toDateString()}
      </p>
      <Posts
        posts={posts}
        postOrder={postOrder.slice(1, postOrder.length)}
      ></Posts>
    </main>
  );
}
