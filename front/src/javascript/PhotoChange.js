import React from "react";
import UrlResolver from "./api/UrlResolver.js";
import RequestBodyBuilder from "./api/RequestBodyBuilder";

const urlResolver = new UrlResolver();
const toBase64 = (file) =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
  });

const submitHandler = async (event, setPhoto) => {
  // const file = URL.createObjectURL(event.target.files[0]);
  const file = await toBase64(event.target.files[0]);
  const username = sessionStorage.getItem("username");
  setPhoto(file);
  const body = {
    username: username,
    image: file,
  };

  const response = await fetch(
    urlResolver.getSetProfilePhotoUrl(sessionStorage.getItem("token")),
    RequestBodyBuilder.getSetProfilePhotoRequestBody(body)
  );
};

export default function PhotoChange({ isSessionUser, setPhoto }) {
  if (!isSessionUser) {
    return <></>;
  }
  return (
    <div className="PhotoChange">
      <input
        type="file"
        accept=".jpg,.jpeg,.png"
        onChange={(e) => submitHandler(e, setPhoto)}
      />
    </div>
  );
}
