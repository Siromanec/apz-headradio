import React from "react";
import FriendSongElement from "./FriendSongElement.js";
import PostBase from "./PostBase.js";
import ProfilePicture from "../data/profile.jpg";
import PostHeader from "./PostHeader.js";
import Post from "./Post.js";

export default function Home() {
  return (
    <div>
      {/* <PostHeader
        headerType="lastPostElement"
        nickName="Beheni"
        avatar={ProfilePicture}
      ></PostHeader>
      <PostBase
        numberLikes={22}
        date={"2 MAY 2023"}
        text={
          "Alonso is greatest driver of all time. Everyone who thinks different — is wrong. He won championships in bad cars and always showed great results. Alonso FTW"
        }
      ></PostBase> */}

      <FriendSongElement
        songName="Окситоцин  •  Ницо Потворно"
        avatar={ProfilePicture}
      ></FriendSongElement>

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
