export default function FileUpload() {
  const changeHandler = () => {};
  return (
    <div className="FileUpload">
      <input type="file" onChange={changeHandler}></input>
    </div>
  );
}
