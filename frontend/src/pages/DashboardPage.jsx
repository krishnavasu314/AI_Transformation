import { useEffect, useState } from "react";
import api from "../api/client";
import Panel from "../components/SectionCard";
import MetricCard from "../components/StatCard";
import { useAuth } from "../context/AuthContext";

const initialTaskForm = { title: "", description: "", assigned_to_id: "" };
const statusCopy = {
  pending: "Open",
  completed: "Completed",
};

function formatDate(value) {
  return new Date(value).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export default function WorkspaceScreen() {
  const { user, logout } = useAuth();
  const isAdmin = user.role === "admin";
  const [analytics, setAnalytics] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [taskForm, setTaskForm] = useState(initialTaskForm);
  const [users, setUsers] = useState([]);
  const [docForm, setDocForm] = useState({ title: "", file: null });
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const loadData = async () => {
    try {
      setIsLoading(true);
      setError("");
      const taskPath = statusFilter ? `/tasks?status=${statusFilter}` : "/tasks";
      const [analyticsRes, tasksRes, docsRes] = await Promise.all([
        api.get("/analytics"),
        api.get(taskPath),
        api.get("/documents"),
      ]);
      setAnalytics(analyticsRes.data);
      setTasks(tasksRes.data);
      setDocuments(docsRes.data);
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Could not load dashboard data.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [statusFilter]);

  useEffect(() => {
    async function loadUsers() {
      try {
        const response = await api.get("/users");
        setUsers(response.data.filter((item) => item.role.name === "user"));
      } catch {
        setUsers([]);
      }
    }

    if (isAdmin) {
      loadUsers();
    }
  }, [isAdmin]);

  const createTask = async (event) => {
    event.preventDefault();
    try {
      await api.post("/tasks", { ...taskForm, assigned_to_id: Number(taskForm.assigned_to_id) });
      setTaskForm(initialTaskForm);
      setNotice("Task created successfully.");
      setError("");
      await loadData();
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Task could not be created.");
    }
  };

  const uploadDocument = async (event) => {
    event.preventDefault();
    try {
      const formData = new FormData();
      formData.append("title", docForm.title);
      formData.append("file", docForm.file);
      await api.post("/documents", formData);
      setDocForm({ title: "", file: null });
      setNotice("Document uploaded and indexed.");
      setError("");
      await loadData();
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Document upload failed.");
    }
  };

  const completeTask = async (taskId, status) => {
    try {
      await api.put(`/tasks/${taskId}`, { status });
      setNotice(`Task marked ${statusCopy[status].toLowerCase()}.`);
      setError("");
      await loadData();
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Task update failed.");
    }
  };

  const runSearch = async (event) => {
    event.preventDefault();
    try {
      const response = await api.post("/search", { query: searchQuery, top_k: 5 });
      setSearchResults(response.data.results);
      setNotice(`Found ${response.data.results.length} matching passages.`);
      setError("");
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Search failed.");
    }
  };

  const completionRate = analytics?.total_tasks
    ? `${Math.round((analytics.completed_tasks / analytics.total_tasks) * 100)}%`
    : "0%";

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">KW</div>
          <div>
            <strong>Knowledge Work</strong>
            <span>{isAdmin ? "Admin workspace" : "Contributor workspace"}</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <button className="nav-item nav-item--active">Overview</button>
          <button className="nav-item">Tasks</button>
          <button className="nav-item">Documents</button>
          <button className="nav-item">Search</button>
        </nav>

        <div className="sidebar-panel">
          <span className="sidebar-label">Signed in as</span>
          <strong>{user.full_name}</strong>
          <span>{user.email}</span>
          <span className="role-pill">{user.role}</span>
        </div>

        <div className="sidebar-panel">
          <span className="sidebar-label">Today</span>
          <strong>{new Date().toLocaleDateString("en-US", { month: "long", day: "numeric" })}</strong>
          <span>{analytics ? `${analytics.total_searches} searches logged` : "Loading activity"}</span>
        </div>

        <button className="ghost-button ghost-button--sidebar" onClick={logout}>
          Logout
        </button>
      </aside>

      <section className="workspace">
        <header className="workspace-header">
          <div>
            <span className="eyebrow">{isAdmin ? "Operations Dashboard" : "My Workspace"}</span>
            <h1>{isAdmin ? "Team activity at a glance" : "Your assignments and reference notes"}</h1>
            <p>
              {isAdmin
                ? "Track task progress, add source material, and support the team with searchable documents."
                : "Review assigned work, search the knowledge base, and update progress as you complete tasks."}
            </p>
          </div>
          <div className="header-summary">
            <span className="summary-label">Completion rate</span>
            <strong>{completionRate}</strong>
          </div>
        </header>

        {notice ? <div className="success-banner">{notice}</div> : null}
        {error ? <div className="error-banner">{error}</div> : null}

        {analytics ? (
          <section className="stats-grid">
            <MetricCard label="Total Tasks" value={analytics.total_tasks} accent="#0f766e" note="Visible in your scope" />
            <MetricCard label="Completed" value={analytics.completed_tasks} accent="#166534" note="Closed work items" />
            <MetricCard label="Pending" value={analytics.pending_tasks} accent="#b45309" note="Still in progress" />
            <MetricCard label="Searches" value={analytics.total_searches} accent="#1d4ed8" note="Queries recorded" />
          </section>
        ) : null}

        <section className="workspace-grid">
          <div className="primary-column">
            <Panel
              title="Task Queue"
              subtitle="Keep assignments moving and filter by status when you need a narrower view."
              action={
                <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
                  <option value="">All tasks</option>
                  <option value="pending">Pending only</option>
                  <option value="completed">Completed only</option>
                </select>
              }
            >
              {isLoading ? <div className="empty-state">Loading tasks...</div> : null}
              {!isLoading && tasks.length === 0 ? <div className="empty-state">No tasks found for this filter.</div> : null}
              <div className="task-list">
                {tasks.map((task) => (
                  <article key={task.id} className="task-row">
                    <div className="task-main">
                      <div className="task-topline">
                        <strong>{task.title}</strong>
                        <span className={`status-chip status-chip--${task.status}`}>{statusCopy[task.status]}</span>
                      </div>
                      <p>{task.description}</p>
                      <div className="task-meta">
                        <span>Assigned to {task.assigned_to.full_name}</span>
                        <span>Created {formatDate(task.created_at)}</span>
                      </div>
                    </div>
                    <div className="task-actions">
                      <button className="secondary-button" onClick={() => completeTask(task.id, "pending")}>
                        Reopen
                      </button>
                      <button onClick={() => completeTask(task.id, "completed")}>Complete</button>
                    </div>
                  </article>
                ))}
              </div>
            </Panel>

            <Panel
              title="Document Search"
              subtitle="Search the indexed knowledge base and pull back the most relevant passages."
              tone="highlight"
            >
              <form className="search-bar" onSubmit={runSearch}>
                <input
                  placeholder="Ask about a process, policy, note, or requirement"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button type="submit">Search</button>
              </form>
              {searchResults.length === 0 ? (
                <div className="empty-state">Run a search to see matching document passages.</div>
              ) : (
                <div className="result-list">
                  {searchResults.map((result, index) => (
                    <article key={`${result.document_id}-${index}`} className="result-card">
                      <div className="result-head">
                        <strong>{result.document_title}</strong>
                        <span className="score-pill">{Math.round(result.score * 100)} match</span>
                      </div>
                      <p>{result.chunk_text}</p>
                    </article>
                  ))}
                </div>
              )}
            </Panel>

            {isAdmin ? (
              <div className="admin-grid">
                <Panel title="Create Task" subtitle="Add a clear work item and assign it to a contributor.">
                  <form className="stack-form" onSubmit={createTask}>
                    <label>
                      Task title
                      <input
                        value={taskForm.title}
                        onChange={(e) => setTaskForm({ ...taskForm, title: e.target.value })}
                      />
                    </label>
                    <label>
                      Description
                      <textarea
                        value={taskForm.description}
                        onChange={(e) => setTaskForm({ ...taskForm, description: e.target.value })}
                      />
                    </label>
                    <label>
                      Assign to
                      <select
                        value={taskForm.assigned_to_id}
                        onChange={(e) => setTaskForm({ ...taskForm, assigned_to_id: e.target.value })}
                      >
                        <option value="">Choose a user</option>
                        {users.map((item) => (
                          <option key={item.id} value={item.id}>
                            {item.full_name} ({item.username})
                          </option>
                        ))}
                      </select>
                    </label>
                    <button type="submit">Save task</button>
                  </form>
                </Panel>

                <Panel title="Add Document" subtitle="Upload a text file so the team can search it later.">
                  <form className="stack-form" onSubmit={uploadDocument}>
                    <label>
                      Document title
                      <input
                        value={docForm.title}
                        onChange={(e) => setDocForm({ ...docForm, title: e.target.value })}
                      />
                    </label>
                    <label>
                      Text file
                      <input
                        type="file"
                        accept=".txt"
                        onChange={(e) => setDocForm({ ...docForm, file: e.target.files?.[0] || null })}
                      />
                    </label>
                    <button type="submit">Upload and index</button>
                  </form>
                </Panel>
              </div>
            ) : null}
          </div>

          <div className="secondary-column">
            <Panel title="Library" subtitle="Recently uploaded documents currently available for retrieval.">
              {documents.length === 0 ? <div className="empty-state">No documents uploaded yet.</div> : null}
              <div className="document-list">
                {documents.map((doc) => (
                  <article key={doc.id} className="document-row">
                    <div>
                      <strong>{doc.title}</strong>
                      <p>{doc.content_preview}</p>
                    </div>
                    <div className="document-meta">
                      <span>{doc.chunk_count} passages</span>
                      <span>{formatDate(doc.created_at)}</span>
                    </div>
                  </article>
                ))}
              </div>
            </Panel>

            <Panel title="Search Trends" subtitle="Queries pulled from the audit trail for quick usage insight.">
              {!analytics?.top_queries?.length ? (
                <div className="empty-state">Search history will appear after users start querying documents.</div>
              ) : (
                <div className="query-list">
                  {analytics.top_queries.map((item) => (
                    <div key={item.query} className="query-row">
                      <span>{item.query}</span>
                      <strong>{item.count}</strong>
                    </div>
                  ))}
                </div>
              )}
            </Panel>
          </div>
        </section>
      </section>
    </main>
  );
}
