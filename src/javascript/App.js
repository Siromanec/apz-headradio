import logo from "../data/logo.svg";
import "../css/App.css";
import { Link, Outlet } from "react-router-dom";
import { useState } from "react";
import  Header from "./Header.js"
import Footer from "./Footer.js"
import { RequireAuth } from "react-auth-kit";
import Login from "./Login.js"
import { useNavigate } from "react-router-dom"
function MyButton() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return <button onClick={handleClick}>Clicked {count} times</button>;
}

function setToken(userToken) {
  sessionStorage.setItem('token', JSON.stringify(userToken));
}

function getToken() {
  const tokenString = sessionStorage.getItem('token');
  const userToken = JSON.parse(tokenString);
  return userToken?.token
}

export default function App() {

  const navigate = useNavigate();

  let token = getToken();
  if(!token) {
    // navigate("/login")
    return <><Login setToken={setToken} /></>
  }

  return (
    <div>
      <Header></Header>
      <Outlet></Outlet>
      <Footer></Footer>
    </div>
  );
}
