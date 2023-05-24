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
import crossButton from "../data/cross.svg";
import { Link, useNavigate } from "react-router-dom";


import {spotifyClientID, spotifyClientSecret} from "./APIKeys";

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
  const { username, avatar, posts, friends, song } = useLoaderData();

  const [isCurrentUser, setIsCurrentUser] = useState(
    username === sessionStorage.getItem("username")
  );
  const [isFriend, setIsFriend] = useState(
    !isCurrentUser && friends.includes(sessionStorage.getItem("username"))
  );

  const [photo, setPhoto] = useState(avatar);
  const [userSong, setUserSong] = useState();
  const songChange = async () => {
    const token = await APIController.getToken()
    const songs =  new URL(song).pathname.split("/").pop();
    const result = await APIController.getTrack(token, songs);
    console.log(result);
    setUserSong(result)
  }
  useEffect(()=>{songChange()}, [])
  const [show, setShow] = useState(false);
  const [date, setDate] = useState(new Date());
  const [friendsCount, setFriendsCount] = useState(friends.length);

  const postOrder = Object.keys(posts.data).sort((a, b) => b - a);
  const [currentPost, setCurrentPost] = useState(posts.data[postOrder[0]]);

  useEffect(()=>{setCurrentPost({
    id: currentPost.idpost,
    username: currentPost.username,
    text: currentPost.article,
    added: currentPost.added,
    numberLikes: currentPost.nlikes,
  });}, []);

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

  const [popUpFriendsCLass, setPopUpFriendsClass] = useState("popup-change");
  function handleShowFriends() {
    console.log(friends);
    setPopUpFriendsClass("popup-change show");
  }
  function exitShowFriends() {
    setPopUpFriendsClass("popup-change");
  }

  const navigate = useNavigate();
  let friendsList = [];
  for (let i = 0; i < friends.length; ++i) {
    friendsList.push(
      <div className="friend">
        <span
          onClick={() => {navigate("/profile/" + friends[i]); exitShowFriends()}}
          className="friend-username"
        >
          {"@" + friends[i]}
        </span>
      </div>
    );
  }
  const handlePhoto = () => {
    setShow((show) => !show);
  };

  async function handleSongClick() {
    console.log(song)
    window.open(song);
  }

  useEffect(() => {
    setIsCurrentUser(username === sessionStorage.getItem("username"));
    setPhoto(avatar);
    setFriendsCount(friends.length);
  }, [username]);
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
          <div
            className={`profilePictureDiv ${
              isCurrentUser ? "can-change-picture" : ""
            }`}
          >
            <span className="editText" onClick={handlePhoto}>
              Change Photo
            </span>
            <img
              src={photo ? photo : DefaultProfile}
              className="profilePicture"
            />
            {show ? (
              <PhotoChange isSessionUser={isCurrentUser} setPhoto={setPhoto} />
            ) : null}
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
              <span
                id="song-name"
                className="songName"
                onClick={handleSongClick}
              >
              {userSong}
              </span>
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
              <div className={popUpFriendsCLass}>
                <div className="FriendsList-div">
                  <div className="FriendsList-header-div">
                    <span className="FriendsList-header">Friends</span>
                    <button className="exitButton" onClick={exitShowFriends}>
                      <img src={crossButton} style={{ width: "20px" }} />
                    </button>
                  </div>
                  <div className="FriendsList-main-div">{friendsList}</div>
                </div>
              </div>
            </div>
          </div>
          {isCurrentUser ? (
            <ChangeSong profile={username} APIController={APIController} setUserSong={setUserSong}/>
          ) : (
            <AddFriend
              profile={username}
              isFriend={isFriend}
              setIsFriend={setIsFriend}
            />
          )}
        </div>
      </section>
      <section className="recentDiary"></section>
      <section className="textField"></section>
      {isCurrentUser && <EditorWrapper></EditorWrapper>}
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
