import React, { useEffect, useState } from "react";
import Post from "./Post.js";

import TripleFriendSong from "./TripleFriendSong.js";
import { Await, useLoaderData, useParams } from "react-router-dom";

function Posts({ posts, postOrder, avatars }) {
  const listItems = posts
    ? postOrder.map((number) => {
        const num = parseInt(number);
        const post = posts[num];
        if (post) {
          const postWrap = {
            id: post["idpost"],
            username: post["username"],
            text: post["article"],
            added: post["added"],
            numberLikes: post["nlikes"],
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
  const { posts, avatars } = useLoaderData();
  const postOrder = posts ? Object.keys(posts).sort((a, b) => b - a) : [];

  return (
    <div>
      <TripleFriendSong></TripleFriendSong>
      <Posts
        headerType="postHeader"
        posts={posts}
        avatars={avatars}
        postOrder={postOrder ? postOrder.slice(0, postOrder.length) : []}
      />
    </div>
  );
}
