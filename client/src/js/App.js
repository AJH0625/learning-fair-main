import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Class from './Class';
import Login from './Login';
import Main from './Main';
import Congrats from './Congrats'
import Tag from './Tag'

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Login />}></Route>
          <Route path="/main" element={<Main />}></Route>
          <Route path="/congrats" element={<Congrats />}></Route>
          <Route path="/tag/:tagId" element={<Tag />}></Route>
          <Route path="/class/:classId" element={<Class />}></Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
