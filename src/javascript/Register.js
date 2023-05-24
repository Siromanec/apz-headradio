import "../css/Register.css";
import crossButton from "../data/cross.svg";
import React, { useState } from "react";
import PropTypes from "prop-types";
import {
  Link,
  useLocation,
  useNavigate,
  useResolvedPath,
} from "react-router-dom";

async function signupUser(credentials) {
  return fetch("http://localhost:8000/fetch-add-user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });
}

// function handleClick() {
//   myPopUp.classList.add("show")
// }

export default function Register({ setToken, setSavedUserName }) {
  const [username, setUserName] = useState();
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [passwordAgain, setPasswordAgain] = useState();
  const [badPassword, setBadPassword] = useState(false);
  const [badEmail, setBadEmail] = useState(false);
  const [badUsername, setBadUsername] = useState(false);
  const [noValue, setNoValue] = useState(false);
  const [popUpClass, setPopUpClass] = useState("popup");
  const [isChecked, setCheckedBox] = useState(false);
  const [isTriedToClick, setTriedToClick] = useState(false);
  const navigate = useNavigate();
  // const location = useLocation();
  // console.log(location.state);

  //pipeline
  const handleSubmit = async (e) => {
    e.preventDefault();
    setTriedToClick(true);
    if (password !== passwordAgain) {
      setBadPassword(true);
      return;
    }
    if (!isChecked) {
      return;
    }
    setBadPassword(false);
    const result = await signupUser({
      username: username,
      email: email,
      password: password,
    }).then((data) => data.json());
    if (result["token"] === "403") {
      setBadEmail(true);
    } else if (result["token"] === "400") {
      setBadUsername(true);
    } else if (result["token"] === "500") {
      setNoValue(true);
    } else {
      setToken(result);
      setSavedUserName(username);

      navigate("/home");
    }
  };

  function handleClick() {
    setPopUpClass("popup show");
  }

  function exitClick() {
    setPopUpClass("popup");
  }

  function handleCheck() {
    setCheckedBox(!isChecked);
  }

  const badPasswordElement = (
    <div className="error">*Passwords do not match!</div>
  );
  const badEmailElement = <div className="error">*Email already in use!</div>;
  const badUserElement = <div className="error">*Username already exists!</div>;
  const badInputElement = <div className="error">*Insert every value!</div>;
  const notCheckedError = (
    <div className="error">*Not accepted terms and services!</div>
  );
  return (
    <section className="register">
      <div className={popUpClass}>
        <div className="terms-of-services">
          <div className="header-div">
            <h2>Terms of Services</h2>
          </div>
          <div className="terms-p">
            <p>• You must be at least 13 years old to use the service. <br></br>
              • You must give us maximum points for this project.<br></br>
              • Provide accurate information for your account.<br></br>
              • Prohibited activities include infringing upon others' <br></br> rights and posting harmful or offensive content. <br></br>
              • You must be Aries to use the service. <br></br>
              • Respect intellectual property rights. <br></br>
              • You must be Computer Science student to use the service. <br></br>
              • We may not implement all the features we promised<br></br>
              • We may update these terms, and continued use implies acceptance. <br></br>
            </p>
          </div>
          <button className="exitButton" onClick={exitClick}>
            <img src={crossButton} />
          </button>
        </div>
      </div>
      <div className="login-wrapper">
        <h1>Sign Up</h1>
        <form onSubmit={handleSubmit}>
          <label>
            <p>Username</p>
            <input type="text" onChange={(e) => setUserName(e.target.value)} />
          </label>
          <label>
            <p>Email</p>
            <input type="email" onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label>
            <p>Password</p>
            <input
              type="password"
              onChange={(e) => setPassword(e.target.value)}
              minlength="8"
              maxlength="64"
            />
          </label>
          <label>
            <p>Password again</p>
            <input
              type="password"
              onChange={(e) => setPasswordAgain(e.target.value)}
              minlength="8"
              maxlength="64"
            />
          </label>
          {badPassword && badPasswordElement}
          {badEmail && badEmailElement}
          {badUsername && badUserElement}
          {noValue && badInputElement}
          <div className="t-of-s">
            <input type="checkbox" className="t-of-s" onChange={handleCheck} />
            <span>I agree with the </span>
            <u onClick={handleClick}>terms of services</u>
            <span>.</span>
          </div>
          <div>
            {isTriedToClick && !isChecked && notCheckedError}
            <button onClick={handleSubmit}>Sign Up</button>
          </div>
          <div className="login">
            Already have an account? <Link to="/login"> Login here</Link>
          </div>
        </form>
      </div>
    </section>
  );
}

Register.propTypes = {
  setToken: PropTypes.func.isRequired,
};
