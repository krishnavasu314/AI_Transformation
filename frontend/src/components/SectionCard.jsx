export default function Panel({ title, subtitle, children, action, tone = "default" }) {
  return (
    <section className={`section-card section-card--${tone}`}>
      <div className="section-head">
        <div>
          <h2>{title}</h2>
          {subtitle ? <p>{subtitle}</p> : null}
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}
