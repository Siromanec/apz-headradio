import "../css/PostHeader.css";

export default function PostHeader({ headerType, nickName, avatar }) {
  if (headerType === "postHeader") {
    return (
      <div className="postHeaderDiv">
        <img className="postHeaderImg" src={avatar}></img>
        <div className="postHeaderLabelDiv">
          <label className="postHeaderLabel">{nickName}</label>
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
