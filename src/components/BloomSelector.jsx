export default function BloomSelector({ values, setValues }) {
  const update = (level, value) => {
    setValues({ ...values, [level]: value / 100 });
  };

  return (
    <div>
      <h4>Bloom’s Taxonomy</h4>
      {Object.keys(values).map((level) => (
        <div key={level}>
          <label>{level}</label>
          <input
            type="range"
            min={0}
            max={100}
            value={values[level] * 100}
            onChange={(e) => update(level, e.target.value)}
          />
        </div>
      ))}
    </div>
  );
}