import React from 'react';
import {
  BrowserRouter as Router,
  Route,
} from "react-router-dom";
import LeftMenu from './components/LeftMenu/LeftMenu'
import Main from './pages/Main/Main'
import styled from '@emotion/styled'

const Wrapper = styled.div`
  display: flex;
  flex-direction: row;
`

function App() {
  return (
    <Router>
      <Wrapper>
        <LeftMenu/>
        <Route exact path='/' render={Main} />
      </Wrapper>
    </Router>
  );
}

export default App;
