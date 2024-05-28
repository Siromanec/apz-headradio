import SendIcon from "../data/send-icon.svg";
import PictureIcon from "../data/picture-icon.svg";
import { Editor } from "@tinymce/tinymce-react";
import { useRef } from "react";
import "../css/Editor.css";
import { tinymceAPIKey } from "./api/APIKeys";
import UrlResolver from "./api/UrlResolver";
import RequestBodyBuilder from "./api/RequestBodyBuilder";
import {getToken} from "./api/Token";

// import { Global } from "@emotion/core";
function getSavedUserName() {
  return sessionStorage.getItem("username");
}

const urlResolver = new UrlResolver();

/**
 * @param articleData.article
 * @param {String} articleData.profile
 * */
async function sendPostContents(articleData) {
    return fetch(urlResolver.getNewPostUrl(getToken()), RequestBodyBuilder.getNewPostRequestBody(articleData)).then((data) => data.json());
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
