import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function SignInScreen() {
  const { login } = useAuth();
  const [form, setForm] = useState({ username: "admin", password: "admin123" });
  const [error, setError] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    try {
      setError("");
      await login(form.username, form.password);
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <main className="login-shell">
      <section className="login-stage">
        <div className="login-copy">
          <span className="eyebrow">Knowledge Workspace</span>
          <h1>Search team documents, manage assigned work, and track progress in one place.</h1>
          <p>
            Built for a lead-and-contributor workflow: admins curate the knowledge base and assign
            tasks, while users search the indexed notes and complete work without switching tools.
          </p>
          <div className="login-feature-list">
            <div>
              <strong>Role-based access</strong>
              <span>Separate admin and contributor flows with JWT-backed sessions.</span>
            </div>
            <div>
              <strong>Document retrieval</strong>
              <span>Search uploaded text using embedding similarity instead of keyword matching.</span>
            </div>
            <div>
              <strong>Task visibility</strong>
              <span>Keep assignments, status, and search activity visible on the same dashboard.</span>
            </div>
          </div>
        </div>

        <div className="login-panel">
          <div className="login-panel-head">
            <div>
              <span className="eyebrow">Sign In</span>
              <h2>Open your workspace</h2>
            </div>
            <span className="env-pill">Local Demo</span>
          </div>

          <form onSubmit={submit} className="login-form">
            <label>
              Username
              <input
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
              />
            </label>
            <label>
              Password
              <input
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
              />
            </label>
            {error ? <div className="error-banner">{error}</div> : null}
            <button type="submit">Sign in</button>
          </form>

          <div className="credential-block">
            <div>
              <span>Admin</span>
              <strong>admin / admin123</strong>
            </div>
            <div>
              <span>User</span>
              <strong>user1 / user123</strong>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
