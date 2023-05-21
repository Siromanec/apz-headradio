import "../css/Footer.css";
import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer>
      <div className="footerDiv">
        <span className="footerText">© 2023 by HeadRadio.</span>
        <div className="footerLinkWrapper">
          <Link to="/home" className="footerLink">
            Home
          </Link>
          <Link to="/profile" className="footerLink">
            Profile
          </Link>
          <Link to="/about" className="footerLink">
            About
          </Link>
        </div>
      </div>
    </footer>
  );
}
