import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import GuestHomePage from "../pages/GuestHomePage";
import UserHomePage from "../pages/UserHomePage";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Contact from "../pages/Contact";
import { UserProvider } from "../pages/context/UserContext";

function App() {
  return (
    <Router>
      <UserProvider>
        <Switch>
          <Route exact path="/" component={GuestHomePage} />
          <Route path="/login" component={Login} />
          <Route path="/register" component={Register} />
          <Route path="/user" component={UserHomePage} />
        </Switch>
      </UserProvider>
    </Router>
  );
}

export default App;