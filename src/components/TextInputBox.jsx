//src/components/TextInputBox.jsx
export default function TextInputBox({ text, setText }) {

  return (

    <div className="text-box">

      <textarea
        placeholder="Paste your text or study material here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={12}
        style={{
          width: "100%",
          padding: "12px",
          fontSize: "14px",
          borderRadius: "6px",
          border: "1px solid #ccc"
        }}
      />

    </div>

  );

}