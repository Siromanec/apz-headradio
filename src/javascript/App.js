import { useState } from "react";
import { RequireAuth } from "react-auth-kit";
import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";

import logo from "../data/logo.svg";
import Footer from "./Footer.js";
import Header from "./Header.js";
import Login from "./Login.js";

import "../css/App.css";

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
  let currentElement;
  if (
    !token &&
    !(
      location.pathname === "/login" ||
      location.pathname === "/about" ||
      location.pathname === "/signup" ||
      !location.pathname.startsWith("/profile")
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
