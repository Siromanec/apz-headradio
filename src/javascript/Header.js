import logo from "../data/logo.svg";
import settingsIcon from "../data/cogwheel.svg";
import "../css/Header.css";
import { Link } from "react-router-dom";
import { useState } from "react";
import SearchInputImg from "../data/search_button.svg"
import SignOutImg from "../data/sign_out.svg"

function SearchInput() {
  return <div class="search">
      <input type="search" placeholder="Search ..."/>
      <img className="searchButton" src={SearchInputImg}/>
        </div>;
}
export default function Header() {
  return (
    <header>
        <div className="titles">
      <h3 className="pretitle">EVERYTHING IS PERSONAL. INCLUDING THIS BLOG.</h3>
      <h1 className="title">HeadRadio</h1>
        </div>
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
          <button className="signOutButton">
            <img className="signOutImg" src={SignOutImg}/>
          </button>
      </div>
    </header>
  );
}
