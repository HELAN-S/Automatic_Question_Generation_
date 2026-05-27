export default function DifficultySliders() {
  return (
    <>
      <label>Difficulty Distribution</label>
      <div className="slider">
        Easy <input type="range" />
      </div>
      <div className="slider">
        Medium <input type="range" />
      </div>
      <div className="slider">
        Hard <input type="range" />
      </div>
    </>
  );
}