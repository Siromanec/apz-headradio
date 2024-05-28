import React, { useEffect, useState } from "react";
import { Await, useLoaderData, useParams } from "react-router-dom";

import Post from "./Post.js";

import TripleFriendSong from "./TripleFriendSong.js";


function Posts({ posts, postOrder, avatars }) {
  const listItems = posts
    ? postOrder.map((number) => {
        const num = parseInt(number);
        const post = posts[num];
        if (post) {
          const postWrap = {
            id: post["postId"],
            username: post["username"],
            text: post["article"],
            added: post["time"],
            numberLikes: post["likeCount"],
            avatar: avatars[post["username"]],
          };
          return (
            <Post headerType="postHeader" post={postWrap} images={null}></Post>
          );
        }
      })
    : null;
  return <>{listItems}</>;
}

export default function Home() {
  const { posts, profilePictures } = useLoaderData();
  const postOrder = posts ? Object.keys(posts).sort((a, b) => b - a) : [];

  return (
    <div>
      {/* <TripleFriendSong></TripleFriendSong> */}
      <Posts
        headerType="postHeader"
        posts={posts}
        avatars={profilePictures}
        postOrder={postOrder ? postOrder.slice(0, postOrder.length) : []}
      />
    </div>
  );
}
