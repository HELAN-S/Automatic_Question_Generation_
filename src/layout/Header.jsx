
export default function Header({ title }) {
  return (
    <header className="header">
      <h1>{title}</h1>
      <div className="profile">👤</div>
    </header>
  );
}