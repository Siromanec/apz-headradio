import blankProfilePicture from "./blank-profile-picture.svg";
import spotifyIcon from "./spotify_icon.svg";
import ReactPlayer from "react-player/lazy";
import ReactAudioPlayer from "react-audio-player";
import song from "./staying-alive.mp3";
function UserIcon() {
  return;
}

export default function Profile() {
  const songName = "Staying Alive";
  return (
    <main>
      <section>
        <div className="profilePictureDiv">
          <img src={blankProfilePicture} className="profilePicture" />
        </div>
        <div className="status">
          <span>Feeling perky</span>
        </div>
      </section>
      <section className="headRadio">
        <div>{songName}</div>
        <img src={spotifyIcon} style={{ width: "50px" }}></img>
        <ReactAudioPlayer src={song} controls />

      </section>
      <section className="recentDiary"></section>
    </main>
  );
}
