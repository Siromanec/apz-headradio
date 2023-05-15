import logo from "./logo.svg";
import settingsIcon from "./cogwheel.svg";
import "./Header.css";
import { Link } from "react-router-dom";
import { useState } from "react";

function SearchInput() {
  return <input type="search" placeholder="Search"></input>;
}
export default function Header() {
  return (
    <header>
      <h3 className="pretitle">EVERYTHING IS PERSONAL. INCLUDING THIS BLOG.</h3>
      <h1 className="title">HeadRadio</h1>
      <div className="headerLinkWrapper">
        <Link to="/home" className="headerLink">
          Home
        </Link>
        <Link to="/profile" className="headerLink">
          Profile
        </Link>
        <Link to="/about" className="headerLink">
          About
        </Link>
        <SearchInput />
      </div>
    </header>
  );
}
