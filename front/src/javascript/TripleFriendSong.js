import "../css/TripleFriendSong.css";
import FriendSongElement from "./FriendSongElement.js";
import ProfilePicture from "../data/profile.jpg";
import ButtonImg from "../data/left-arrow.svg";

export default function TripleFriendSong() {
  return (
    <div className="TripleGeneralDiv">
      <button className="TripleFriendButton">
        <img className="LeftButtonImg" src={ButtonImg}></img>
      </button>
      <div className="TripleFriendSongDiv">
        <div className="FirstFriendSong">
          <FriendSongElement
            songName="Окситоцин  •  Ницо Потворно"
            avatar={ProfilePicture}
          ></FriendSongElement>
        </div>
        <div className="SecondFriendSong">
          <FriendSongElement
            songName="Окситоцин  •  Ницо Потворно"
            avatar={ProfilePicture}
          ></FriendSongElement>
        </div>
        <div className="ThirdFriendSong">
          <FriendSongElement
            songName="Окситоцин  •  Ницо Потворно"
            avatar={ProfilePicture}
          ></FriendSongElement>
        </div>
      </div>
      <button className="TripleFriendButton">
        <img className="RightButtonImg" src={ButtonImg}></img>
      </button>
    </div>
  );
}
