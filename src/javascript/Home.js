import React from "react";
import FriendSongElement from "./FriendSongElement.js";
import PostBase from "./PostBase.js";
import ProfilePicture from "../data/profile.jpg";
import PostHeader from "./PostHeader.js";
import Post from "./Post.js";
import TripleFriendSong from "./TripleFriendSong.js";

export default function Home() {
  return (
    <div>
      <TripleFriendSong></TripleFriendSong>
      <Post
        headerType="lastPostElement"
        nickName="Beheni"
        avatar={ProfilePicture}
        text={
          "Alonso is greatest driver of all time. Everyone who thinks different — is wrong. He won championships in bad cars and always showed great results. Alonso FTW"
        }
        date={"2 MAY 2023"}
        numberLikes={22}
      ></Post>

      <Post
        headerType="postHeader"
        nickName="Beheni"
        avatar={ProfilePicture}
        text={
          "Alonso is greatest driver of all time. Everyone who thinks different — is wrong. He won championships in bad cars and always showed great results. Alonso FTW"
        }
        date={"2 MAY 2023"}
        numberLikes={22}
      ></Post>
    </div>
  );
}
