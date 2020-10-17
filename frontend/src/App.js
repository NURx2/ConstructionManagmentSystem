import React from 'react';
import {
  BrowserRouter as Router,
  Route,
} from "react-router-dom";
import LeftMenu from './components/LeftMenu/LeftMenu'
import Main from './pages/Main/Main'

function App() {
  return (
    <Router>
      <LeftMenu/>
      <Route exact path='/' render={Main} />
    </Router>
  );
}

export default App;
