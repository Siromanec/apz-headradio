import logo from "../data/logo.svg";
import "../css/App.css";
import { Link, Outlet } from "react-router-dom";
import { useState } from "react";
import Header from "./Header.js";
import Footer from "./Footer.js";
import { RequireAuth } from "react-auth-kit";
import Login from "./Login.js";
import { useNavigate, useLocation } from "react-router-dom";
function MyButton() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return <button onClick={handleClick}>Clicked {count} times</button>;
}

function resetToken() {
  sessionStorage.setItem("token", JSON.stringify(null));
}

function getToken() {
  const tokenString = sessionStorage.getItem("token");
  if (!tokenString) return undefined;
  const userToken = JSON.parse(tokenString);
  return userToken?.token;
}

export default function App() {
  const navigate = useNavigate();
  const location = useLocation();

  const token = getToken();
  // console.log(token) ;
  let currentElement;
  if (
    !token &&
    !(
      location.pathname === "/login" ||
      location.pathname === "/about" ||
      location.pathname === "/signup"
    )
  ) {
    navigate("/login");
  } else {
  }

  function onSignOut() {
    resetToken();
    navigate("/login");
  }

  return (
    <div>
      <Header onSignOut={onSignOut} isSignedOut={!token}></Header>
      <Outlet></Outlet>
      <Footer isSignedOut={!token}></Footer>
    </div>
  );
}
