import React from 'react';
import Logo from "assets/images/MuralLogo_M.svg";
import { Link,useLocation } from 'react-router-dom';


const Navbar: React.FC = () => {
  const location = useLocation();
  
  return (
  <div className="navbar bg-base-100 shadow-sm">
    <div className="navbar-start">
      <img src={Logo} className="w-25 h-13 m-3.5"></img>

      <Link to="/" className={`btn btn-link no-underline text-inherit hover:no-underline hover:text-inherit ${location.pathname === "/" ? "btn-active" : ""}`}>
        Home
      </Link>

      <Link to='/Academicos' className={`btn btn-link no-underline text-inherit hover:no-underline hover:text-inherit ${location.pathname === "/Academicos" ? "btn-active" : ""}`}>
        Acadêmicos
      </Link>
      
      <Link to='/Profissionais' className={`btn btn-link no-underline text-inherit hover:no-underline hover:text-inherit ${location.pathname === "/Profissionais" ? "btn-active" : ""}`}>
        Profissionais
      </Link>
    
    </div>

    <div className="navbar-end">
      <input type="text" placeholder="Search" className="input input-bordered-base-300 w-24 md:w-auto " />
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mx-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
    </div>
  </div>
  );
};

export default Navbar;
