
import "../css/Header.css";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import SearchInputImg from "../data/search_button.svg";
import SignOutImg from "../data/sign_out.svg";

import UrlResolver from "./api/UrlResolver.js";
import RequestBodyBuilder from "./api/RequestBodyBuilder";
import {getToken} from "./api/Token";
const urlResolver = new UrlResolver();

function SearchInput() {
  const [exists, setExists] = useState(false)
  const [text, setText] = useState("")
  const [message, setMessage] = useState()
  const navigate = useNavigate()
  const searchHandler = async ()=>{
    // const data = await (fetch(`http://localhost:8000/show-user/${text}`)).then(data => data.json()).then(data => data).catch(e =>console.log(e));
    const data = await (fetch(urlResolver.getShowUserUrl(text, getToken()),
                              RequestBodyBuilder.getShowUserRequestBody())).then(data => data.json()).then(data => data).catch(e =>console.log(e));
    if (Object.keys(data).length!==0){
      setExists(true);
      navigate("/profile/"+text);
      setMessage(null);
      return;
    }
    else{
      setExists(false);
      setMessage("No such user")
      return;
    }
  }
  const textHandler = (event) => {
    setText(event.target.value)
  }
  return <div className="search">
    <input type="search" name="input" placeholder="Search..." onChange={textHandler}/>
    <button className="searchBtn" onClick={searchHandler} ><img className="searchImg" src={SearchInputImg} /></button>
    {message}
  </div>;
}
// export default function Header() {
//   return (
//     <div className="search">
//       <input type="search" placeholder="Search ..." />
//       <img src={SearchInputImg} />
//     </div>
//   );
// }
export default function Header({ onSignOut, isSignedOut }) {
  const [search, setSearch] = useState();

  const lane = (
    <div className="headerLinkWrapper">
      <div className="emptyPart">
        </div>
      <Link to="/home" className="headerLink">
        Home
      </Link>
      <Link to={`/profile/${sessionStorage.getItem("username")}`}  className="headerLink">
        Profile
      </Link>
      <Link to="/about" className="headerLink">
        About
      </Link>
      <SearchInput />
      <div className="emptyPart">
          <div className="getOut">
            <button className="signOutButton" onClick={onSignOut}>
              <img className="signOutImg" src={SignOutImg} />
            </button>
          </div>
        </div>
    </div>
  );
  return (
    <header>
      <div className="titles">
        <h3 className="pretitle">EVERYTHING IS PERSONAL. INCLUDING THIS BLOG.</h3>
        <h1 className="title">HeadRadio</h1>
      </div>
      {!isSignedOut && lane}
      
    </header>
  );
}
