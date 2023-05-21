import logo from "../data/logo.svg";
import "../css/App.css";
import { Link, Outlet } from "react-router-dom";
import { useState } from "react";
import  Header from "./Header.js"
import Footer from "./Footer.js"
function MyButton() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return <button onClick={handleClick}>Clicked {count} times</button>;
}


export default function App() {
  const hello = "hello";
  let i = 0;
  // return (
  //   <div className="App">
  //     <header className="App-header">
  //       <img src={logo} className="App-logo" alt="logo" />
  //       <p>
  //         Edit <code>src/App.js</code> and save to reload.
  //       </p>
  //       <a
  //         className="App-link"
  //         href="https://reactjs.org"
  //         target="_blank"
  //         rel="noopener noreferrer"
  //       >
  //         Learn React
  //       </a>
  //     </header>
  //     {hello}

  //   </div>
  // );
  return (
    <div>
      <Header></Header>
      <Outlet></Outlet>
      <Footer></Footer>
      {/* <MyButton /> */}
    </div>
  );
}
