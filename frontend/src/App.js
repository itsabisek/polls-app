import React, { Component } from 'react'
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import './App.css';
import 'antd/dist/antd.css';
import CustomLayout from './containers/Layout';
import LoginForm from './components/LoginForm';
import { QuestionList } from './containers/QuestionList';
import SignUpForm from './components/SignUpForm';
import { PollsProvider } from './components/PollsContext';


export class App extends Component {
  render() {
    return (
      <PollsProvider>
        <div className="App">
          <Router>
            <CustomLayout >
              <Switch>
                <Route exact path='/' component={QuestionList} />
                <Route path='/login' component={LoginForm} />
                <Route path='/signup' component={SignUpForm} />
              </Switch>
            </CustomLayout>
          </Router>
        </div>
      </PollsProvider>
    )
  }
}

export default App;
