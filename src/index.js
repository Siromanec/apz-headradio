import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import ClickCounter from "./javascript/ClickCounter";
import reportWebVitals from "./javascript/reportWebVitals";
import { BrowserRouter , createBrowserRouter, RouterProvider} from "react-router-dom";
import Home from "./javascript/Home";
import Profile from "./javascript/Profile";
import About from "./javascript/About";

import App from "./javascript/App";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/home",
        index: true,
        element: <Home />
      },
      {
        path: "/profile",
        index: true,
        element: <Profile />
      },
      {
        path: "/about",
        index: true,
        element: <About />
      },
    ],
  },
]);
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <React.StrictMode>
      <RouterProvider router={router} />
    </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
