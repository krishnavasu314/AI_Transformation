import { useAuth } from "./context/AuthContext";
import WorkspaceScreen from "./pages/DashboardPage";
import SignInScreen from "./pages/LoginPage";

export default function App() {
  const { user } = useAuth();
  return user ? <WorkspaceScreen /> : <SignInScreen />;
}
