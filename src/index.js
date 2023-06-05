import React from "react";
import { AuthProvider, RequireAuth } from "react-auth-kit";
import ReactDOM from "react-dom/client";
import {
  BrowserRouter,
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import About from "./javascript/About";
import App from "./javascript/App";
import Home from "./javascript/Home";
import Login from "./javascript/Login";
import Profile from "./javascript/Profile";
import Register from "./javascript/Register";
import reportWebVitals from "./javascript/reportWebVitals";

import "./index.css";

function setToken(userToken) {
  sessionStorage.setItem("token", JSON.stringify(userToken));
}

function setSavedUserName(username) {
  sessionStorage.setItem("username", username);
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/home",
        index: true,
        element: <Home />,
        loader: async () => {
          const data = await fetch("http://localhost:8000/fetch-main-page", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: sessionStorage.getItem("username"),
            }),
          }).then((data) => data.json());
          const posts = data.posts;
          const avatars = data.avatars;

          return { posts, avatars };
        },
      },
      {
        path: "/profile/:username",
        index: true,
        element: <Profile />,
        loader: async ({ params }) => {
          const apiUrl = `http://localhost:8000/fetch-show-user/${params.username}`;
          const data = await (await fetch(apiUrl)).json();
          return data;
        },
      },
      {
        path: "/about",
        index: true,
        element: <About />,
      },
      {
        path: "/login",
        index: true,
        element: (
          <Login setToken={setToken} setSavedUserName={setSavedUserName} />
        ),
      },
      {
        path: "/signup",
        index: true,
        element: (
          <Register setToken={setToken} setSavedUserName={setSavedUserName} />
        ),
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

reportWebVitals();
