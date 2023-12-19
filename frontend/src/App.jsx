/*
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at https://developer.cisco.com/docs/licenses.
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
*/

import './App.css';
import Layout from './layout/layout';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/body/pages/home/home'; // Adjust the path as necessary
import AppPage from './components/body/pages/app/app'; // Adjust the path as necessary

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/app" element={<AppPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
