import "../css/PostHeader.css";
import { Link, useNavigate } from "react-router-dom";

// function headerFriendHeandler() {
//   navigate("/profile/" + text);
// }
export default function PostHeader({ headerType, username, avatar }) {
  const navigate = useNavigate();
  if (headerType === "postHeader") {
    return (
      <div onClick={() => { navigate("/profile/" + username); }} className="postHeaderDiv">
       {/* <div className="postHeaderDiv"> */}
        <img className="postHeaderImg" src={avatar}></img>
        <div className="postHeaderLabelDiv">
          <label className="postHeaderLabel">{username}</label>
        </div>
      </div>
    );
  }

  if (headerType === "lastPostElement") {
    return (
      <div className="lastPostDiv">
        <div className="lastPostLabelDiv">
          <label className="lastPostLabel">LAST POST</label>
        </div>
      </div>
    );
  }

  // <PostHeader headerType={}></PostHeader>
}
