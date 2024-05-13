import SendIcon from "../data/send-icon.svg";
import PictureIcon from "../data/picture-icon.svg";

import { Editor } from "@tinymce/tinymce-react";
import { useRef } from "react";
import "../css/Editor.css";
import { tinymceAPIKey } from "./APIKeys";
// import { Global } from "@emotion/core";
function getSavedUserName() {
  return sessionStorage.getItem("username");
}
import UrlResolver from "../UrlResolver.js";

const urlResolver = new UrlResolver();

async function sendPostContents(articleData) {
  // return fetch("http://localhost:8000/new-post", {
    return fetch(urlResolver.getNewPostUrl(), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(articleData),
  }).then((data) => data.json());
}

export default function EditorWrapper() {
  const editorRef = useRef(null);
  const save = async () => {
    const content = editorRef.current.getContent();
    editorRef.current.setContent("");
    const response = await sendPostContents({
      article: content,
      username: getSavedUserName(),
    });
  };
  return (
    <div className="EditorDiv">
      <Editor
        apiKey={tinymceAPIKey}
        initialValue=""
        onInit={(evt, editor) => (editorRef.current = editor)}
        init={{
          menubar: false,
          statusbar: false,
          quickbars_insert_toolbar: false,
          quickbars_selection_toolbar: false,
          quickbars_image_toolbar: false,
          plugins: ["quickbars"],
          toolbar: "blocks | bold italic strikethrough",
          content_css: "../css/Editor.css",
          selector: "#postEditor", // change this value according to your HTML
          a_plugin_option: true,
          a_configuration_option: 400,
          hidden_input: true,
          setup: function (editor) {
            editor.on("submit", function (e) {
              // console.log("submit event", e);
            });
          },
        }}
        //   onChange={onChange}
      />

      <button className="EditorSubmitButton" onClick={save}>
        <img className="EditorSubmitImg" src={SendIcon}></img>
      </button>
    </div>
  );
}
