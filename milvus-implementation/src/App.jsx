import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import './components/Searchbar/index';
import Searchbar from './components/Searchbar/index.jsx';
import Sidebar from './components/Sidebar/index.jsx';

function App() {
 

  return (
    <>
      <Searchbar></Searchbar>
      <Sidebar></Sidebar>
    </>
  )
}

export default App
