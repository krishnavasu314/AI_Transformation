export default function MetricCard({ label, value, accent, note }) {
  return (
    <div className="stat-card">
      <span className="stat-label">{label}</span>
      <strong className="stat-value" style={{ color: accent }}>
        {value}
      </strong>
      {note ? <span className="stat-note">{note}</span> : null}
    </div>
  );
}
