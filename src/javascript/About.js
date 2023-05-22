import "../css/About.css";
import TeamPicture from "../data/we.jpg";

export default function About() {
  return (
    <div className="AboutGeneralDiv">
      <div className="AboutLabelPictureDiv">
        <div className="AboutLabelDiv">
          <label className="AboutLabel">OUR TEAM</label>
        </div>

        <img src={TeamPicture} className="AboutPicture"></img>
        <p className="AboutText">Feel free to shitpost...</p>
      </div>
    </div>
  );
}
