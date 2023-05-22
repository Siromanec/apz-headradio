import React, { useState } from "react";
import PropTypes from "prop-types";
import { Link, useLocation, useNavigate } from "react-router-dom";

async function loginUser(credentials) {
  return fetch("http://localhost:8000/fetch-login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  }).then((data) => data.json());
}

export default function Login({ setToken, setSavedUserName }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();
  const [badInput, setBadInput] = useState(false);

  const navigate = useNavigate();
  // const location = useLocation();
  // console.log(location.state);
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username) {
      return;
    }
    if (!password) {
      return;
    }
    const token = await loginUser({
      username,
      password,
    });
    console.log(token);
    if (!token) {
      setBadInput(true);
      return;
    }

    setBadInput(false);
    setToken(token);
    setSavedUserName(username);
    navigate("/home");
  };
  const badInputElement = (
    <div className="login-error">Incorrect username or password</div>
  );
  const noUsernameElement = (
    <div className="login-error">please enter username</div>
  );
  const noPasswordElement = (
    <div className="login-error">please enter password</div>
  );

  return (
    <div className="login-wrapper">
      <h1>Please Log In</h1>
      <form onSubmit={handleSubmit}>
        {badInput && badInputElement}
        <label>
          <p>Username</p>
          <input type="text" onChange={(e) => setUserName(e.target.value)} />
        </label>
        {username === "" && noUsernameElement}
        <label>
          <p>Password</p>
          <input
            type="password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {password === "" && noPasswordElement}
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
