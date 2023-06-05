import spotifyIcon from "../data/spotify_icon.svg";
import "../css/FriendSongElement.css";

export default function FriendSongElement({ songName, avatar }) {
  return (
    <div className="FriendSongElementDiv">
      <img className="FriendSongElementAvatar" src={avatar}></img>
      <div className="SongImgTextDiv">
        <img
          className="FriendSongElementImg"
          src={spotifyIcon}
          style={{ width: "40px" }}
        ></img>
        <div className="FriendSongElementTextDiv">
          <label className="FriendSongElementText">{songName}</label>
        </div>
      </div>
    </div>
  );
}
