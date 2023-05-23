import FriendSongElement from "./FriendSongElement.js";
import PostBase from "./PostBase.js";
import React, { useState } from "react";
import ProfilePicture from "../data/profile.jpg";
import PostHeader from "./PostHeader.js";
import "../css/Post.css";




export default function Post({
  post,
}) {

  return (
    <div className="PostDiv">
      <div className="PostHeaderDiv">
        <PostHeader
          className="PostHeader"
          headerType={post.headerType}
          username={post.username}
          avatar={post.avatar}
        ></PostHeader>
      </div>

      <PostBase nlikes={post.numberLikes} date={post.added} article={post.text} id={post.id} username={post.username}></PostBase>
    </div>
  );
}
