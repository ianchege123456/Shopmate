
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Profile from './Components/Profile';
import Support from './Components/Support';
import Error404 from './Components/PrivateRoute';

function App() {
  return (
    <Routes>
      <Route path='/profile' element={<Profile />} />
      <Route path='/support' element={<Support />} />
      {/* Catch all undefined routes and render Error404 component */}
      <Route path='*' element={<Error404 />} />
    </Routes>
  );
}

export default App;
