import "../css/Footer.css";
import { Link, useNavigate, useLocation } from "react-router-dom";

export default function Footer({ isSignedOut }) {
  const navigate = useNavigate();
  const location = useLocation();
  const homeLink = (
    <Link to="/home" className="footerLink">
      Home
    </Link>
  );
  const profileLink = (
    <Link to="/profile" className="footerLink">
      Profile
    </Link>
  );
  const loginLink = (
    <Link to="/login" className="footerLink">
      Login
    </Link>
  );
  const signUpLink = (
    <Link to="/signup" className="footerLink">
      Sign Up
    </Link>
  );
  const aboutLink = (
    <Link to="/about" className="footerLink">
      About
    </Link>
  );

  return (
    <footer>
      <div className="footerDiv">
        <span className="footerText">© 2023 by HeadRadio.</span>
        <div className="footerLinkWrapper">
          {!isSignedOut && homeLink}
          {!isSignedOut && profileLink}
          {isSignedOut && loginLink}
          {isSignedOut && signUpLink}
          {aboutLink}
        </div>
      </div>
    </footer>
  );
}
