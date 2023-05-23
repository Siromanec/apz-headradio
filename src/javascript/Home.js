import React, { useEffect, useState } from "react";
import Post from "./Post.js";
import TripleFriendSong from "./TripleFriendSong.js";

function Posts({ posts, postOrder }) {
  const listItems = posts ? postOrder.map((number) => {  
    const num = parseInt(number)
    const post = posts[num];
    if (post) {
      const postWrap = {
        id: post["idpost"],
        username: post["username"],
        text: post["article"],
        added: post["added"],
        numberLikes: post["nlikes"],
      };
      return <Post headerType="postHeader" post={postWrap} images={null}></Post>;
    }
  }): null;
  return <>{listItems}</>;
}

export default function Home() {
  const postsHandler = async () => {
    const data = await fetch("http://localhost:8000/fetch-main-page", 
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({"username": sessionStorage.getItem("username")}),
    });
    const listPosts = await data.json().then((data)=> data["posts"])
    setPosts(listPosts)
  }
  const [posts, setPosts] = useState(postsHandler);
  const postOrder = posts ? Object.keys(posts).sort((a, b) => b - a): [];

  return (
    <div>
      <TripleFriendSong></TripleFriendSong>
      <Posts headerType="postHeader" posts={posts} postOrder={postOrder ? postOrder.slice(1, postOrder.length) : []}/>
    </div>
  );
}
