import React from "react";
import ReactDOM from "react-dom/client";
import UrlResolver from "./javascript/UrlResolver";
import RequestBodyBuilder from "./javascript/RequestBodyBuilder";
import {createBrowserRouter, RouterProvider,} from "react-router-dom";

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

const urlResolver = new UrlResolver();

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
          const data = await fetch(
              urlResolver.getMainPageUrl(sessionStorage.getItem("username"), sessionStorage.getItem("token")),
              RequestBodyBuilder.getMainPageRequestBody()
              )
              .then((data) => data.json());
          const posts = data.posts;
          const avatars = data.profilePictures;

          return { posts, avatars };
        },
      },
      {
        path: "/profile/:username",
        index: true,
        element: <Profile />,
        loader: async ({ params }) => {
          const apiUrl = urlResolver.getShowUserUrl(params.username,
                                                           sessionStorage.getItem("token"));
          // TODO query for user friend, user posts, and user data
          return await (
              await fetch(apiUrl,
                  RequestBodyBuilder.getShowUserRequestBody())).json();
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
