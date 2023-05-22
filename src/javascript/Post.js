import FriendSongElement from "./FriendSongElement.js";
import PostBase from "./PostBase.js";
import React, { useState } from "react";
import ProfilePicture from "../data/profile.jpg";
import PostHeader from "./PostHeader.js";
import "../css/Post.css";




export default function Post({
  idpost,
  headerType,
  username,
  avatar,
  images,
  text,
  added,
  nlikes,
}) {

  return (
    <div className="PostDiv">
      <div className="PostHeaderDiv">
        <PostHeader
          className="PostHeader"
          headerType={headerType}
          username={username}
          avatar={avatar}
        ></PostHeader>
      </div>

      <PostBase nlikes={nlikes} date={added} text={text} id={idpost} username={username}></PostBase>
    </div>
  );
}
