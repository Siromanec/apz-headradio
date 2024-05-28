import React from "react";
import ReactDOM from "react-dom/client";
import {createBrowserRouter, RouterProvider,} from "react-router-dom";


import UrlResolver from "./javascript/api/UrlResolver";
import RequestBodyBuilder from "./javascript/api/RequestBodyBuilder";

import About from "./javascript/About";
import App from "./javascript/App";
import Home from "./javascript/Home";
import Login from "./javascript/Login";
import Profile from "./javascript/Profile";
import Register from "./javascript/Register";
import reportWebVitals from "./javascript/reportWebVitals";

import "./index.css";
import {getToken, resetToken, setToken} from "./javascript/api/Token";


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
              urlResolver.getMainPageUrl(sessionStorage.getItem("username"), getToken()),
              RequestBodyBuilder.getMainPageRequestBody()
              )
              .then((data) => data.json());
          const posts = data.posts;
          const profilePictures = data.profilePictures;

          return { posts:posts, profilePictures:profilePictures };
        },
      },
      {
        path: "/profile/:username",
        index: true,
        element: <Profile />,
        loader: async ({ params }) => {
          // TODO query for user friend, user posts, and user data
          const profilePromise = fetch(
              urlResolver.getShowUserUrl(params.username,
                                         getToken()),
              RequestBodyBuilder.getShowUserRequestBody());
          const friendsPromise = fetch(
                                                            urlResolver.getGetFriendsUrl(params.username,
                                                                                         getToken()),
                                                            RequestBodyBuilder.getGetFriendsRequestBody());
           // const posts_promise

          return await Promise.all([profilePromise, friendsPromise])
              .then(([profileRaw, friendsRaw]) => {
                return { profile: profileRaw.json(), friends: friendsRaw.json() };
              });

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
