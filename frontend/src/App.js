import React, { Component } from 'react'
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import './App.css';
import 'antd/dist/antd.css';
import CustomLayout from './containers/Layout';
import LoginForm from './components/LoginForm';
import SignUpForm from './components/SignUpForm';
import { PollsProvider } from './components/PollsContext';
import Dashboard from './components/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import Index from './components/Index';
import Logout from './components/Logout';
import UserAsked from './components/UserAsked';
import UserAnswered from './components/UserAnswered';


export class App extends Component {
  render() {
    return (
      <PollsProvider>
        <div className="App">
          <Router>
            <Switch>
              <Route exact path='/' component={Index} />
              <Route path='/login' component={LoginForm} />
              <Route path='/signup' component={SignUpForm} />
              <ProtectedRoute exact path='/user' component={Dashboard} />
              <ProtectedRoute exact path='/user/asked' component={UserAsked} />
              <ProtectedRoute exact path='/user/answered' component={UserAnswered} />
              <ProtectedRoute path='/logout' component={Logout} />
            </Switch>
          </Router>
        </div>
      </PollsProvider>
    )
  }
}

export default App;
