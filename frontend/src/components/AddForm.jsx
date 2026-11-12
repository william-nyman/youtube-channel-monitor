export default function AddForm(props) {
  return (
    <form
      className="add-channel-form"
      onSubmit={(event) => props.handleSubmitClick(event)}
    >
      <input
        className="add-channel-input"
        type="text"
        placeholder="@handle..."
        name="handle"
      ></input>
      <input className="add-channel-submit" type="submit" value="Add"></input>
    </form>
  );
}
