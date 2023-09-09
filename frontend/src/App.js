import './App.css';
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate
} from 'react-router-dom';
import Teacher from './Teacher';
import Student from './Student';

function App() {
  return (
    <div className="App">
      <Router>
          <Routes>
            <Route path="/teacher" exact element={<Teacher />} />
            <Route path="/student" exact element={<Student />} />
          </Routes>
        </Router>
    </div>
  );
}

export default App;
