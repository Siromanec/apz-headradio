import FriendSongElement from "./FriendSongElement.js";
import PostBase from "./PostBase.js";
import ProfilePicture from "../data/profile.jpg";
import PostHeader from "./PostHeader.js";
import "../css/Post.css";

export default function Post({
  headerType,
  nickName,
  avatar,
  photos,
  text,
  date,
  numberLikes,
}) {
  return (
    <div className="PostDiv">
      <div className="PostHeaderDiv">
        <PostHeader
          className="PostHeader"
          headerType={headerType}
          nickName={nickName}
          avatar={avatar}
        ></PostHeader>
      </div>

      <PostBase numberLikes={numberLikes} date={date} text={text}></PostBase>
    </div>
  );
}
