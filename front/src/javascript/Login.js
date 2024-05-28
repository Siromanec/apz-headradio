import "../css/Login.css";
import React, { useState } from "react";
import PropTypes from "prop-types";
import { Link, useLocation, useNavigate } from "react-router-dom";

import UrlResolver from "./api/UrlResolver";
import RequestBodyBuilder from "./api/RequestBodyBuilder";

const urlResolver = new UrlResolver();

/**
 * @param {String} credentials.username
 * @param {String} credentials.password
 * */
async function loginUser({username, password}) {
  return fetch(urlResolver.getLoginUrl(username, password),
      RequestBodyBuilder.getLoginRequestBody());
}

export default function Login({ setToken, setSavedUserName }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();
  const [badUsername, setBadUsername] = useState(false);
  const [badPassword, setBadPassword] = useState(false);
  const [unauthorized, setUnauthorized] = useState(false);
  const [unknownError, setUnknownError] = useState(false);

  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();

    setUnauthorized(false);
    setUnknownError(false);
    setBadUsername(false);
    setBadPassword(false);

    if (!username) {
      setBadUsername(true)
    }
    if (!password) {
      setBadPassword(true)
    }
    if (!(username && password)) {
      return;
    }
    await loginUser({
      username:username,
      password:password,
    })
        .then((response) => {
          if (response.status === 200) {
            return response.json();
          }

          switch (response.status) {
            case 401:
              setUnauthorized(true);
              break;
            default:
              setUnknownError(true);
              break;
          }
          console.log(response)
          throw new Error(response.statusText);
        })
        .then(json => json.token)
        .then(token => {
          setToken(token);
          setSavedUserName(username);
          navigate("/home");
        })
        .catch(err => {
          console.error(err)
        });
  };
  const badInputElement = (
    <div className="error">*Incorrect username or password</div>
  );
  const unknownErrorElement = <div className="error">*Unknown error!</div>;
  const noUsernameElement = <div className="error">*Please enter username</div>;
  const noPasswordElement = <div className="error">*Please enter password</div>;

  return (
    <div className="login-wrapper">
      <h1>Please Log In</h1>
      <form onSubmit={handleSubmit}>
        {unauthorized && badInputElement}
        {unknownError && unknownErrorElement}
        <label>
          <p>Username</p>
          <input type="text" onChange={(e) => setUserName(e.target.value)} />
        </label>
        {badUsername && noUsernameElement}
        <label>
          <p>Password</p>
          <input
            type="password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {badPassword && noPasswordElement}
        <div>
          <button type="submit">Sign In</button>
        </div>
      </form>
      <div className="signup">
        Do not have an account? <Link to="/signup">Register here</Link>
      </div>
    </div>
  );
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired,
};
