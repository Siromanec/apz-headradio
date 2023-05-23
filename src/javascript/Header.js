import logo from "../data/logo.svg";
import settingsIcon from "../data/cogwheel.svg";
import "../css/Header.css";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import SearchInputImg from "../data/search_button.svg";
import SignOutImg from "../data/sign_out.svg";
import userEvent from "@testing-library/user-event";


function SearchInput() {
  const [exists, setExists] = useState(false)
  const [text, setText] = useState("")
  const navigate = useNavigate()
  const searchHandler = async ()=>{
    const data = await (await fetch(`http://localhost:8000/fetch-show-user/${text}`)).json();
    console.log(data);
    if (data["detail"]!=="Not Found"){
      setExists(true);
    }
    else{
      setExists(false);
    }
  }
  const textHandler = (event) => {
    setText(event.target.value)
  }
  return <div className="search">
    <input type="search" name="input" placeholder="Search..." onClick={searchHandler} onChange={textHandler}/>
    <img className="searchButton" src={SearchInputImg} />
    {exists? "user exists" : "No such user" }
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
