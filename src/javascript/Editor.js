import { Editor } from "@tinymce/tinymce-react";
import { useRef } from "react";
import "../css/mycontent.css"
import {tinymceAPIKey} from "./APIKeys"
// import { Global } from "@emotion/core";
export default function EditorWrapper() {
  const editorRef = useRef(null);
  const save = () => {
    // if (editorRef.current) {
        console.log(editorRef)
      const content = editorRef.current.getContent();
      editorRef.current.setContent("");
      // an application would save the editor content to the server here
      console.log(content);
    // }
  };
  return (
    <div>
      <Editor
        apiKey={tinymceAPIKey}
        initialValue=""
        onInit={(evt, editor) => editorRef.current = editor}
        init={{
        content_css: "./mycontent.css",
          selector: "#postEditor", // change this value according to your HTML
          // menubar: 'edit',
          a_plugin_option: true,
          a_configuration_option: 400,
          hidden_input: true,
          setup: function (editor) {
            editor.on("submit", function (e) {
              console.log("submit event", e);
            });
          },
        }}
        //   onChange={onChange}
      />
      <button onClick={save}>Submit</button>
    </div>
  );
}
// для картинок би окремий механізм
