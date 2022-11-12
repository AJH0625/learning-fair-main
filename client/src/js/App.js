import { BrowserRouter as Router,Route, Routes} from 'react-router-dom';
import Login from './Login';
import Layout from './layouts/layout';
// import Main from './Main';
// import Class from './Class';
// import Project from './Project';
// import Congrats from './Congrats'
// import Tag from './Tag'
// import Awards from './Awards';
function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Login />}></Route>
          <Route path="/*" element={<Layout />} /> 
         {/* <Route path="*" element={<NotFound />} /> */}
        </Routes>
      </Router>
    </div>
  );
}

export default App;
