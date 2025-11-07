import { AppProvider } from './context/AppContext';
import DashboardPage from './pages/DashboardPage';
import './App.css';

function App() {
  return (
    <AppProvider>
      <DashboardPage />
    </AppProvider>
  );
}

export default App;