import React, { useEffect, useRef } from "react";
import Typed from "typed.js";
import flight from "../../../icons/flight.svg";
import "./Navbar.css";

function Navbar({ onLoginClick }) {
  const el = useRef(null);

  useEffect(() => {
    const typed = new Typed(el.current, {
      strings: [
        "Hello!^1000",
        "We are <b>Weir</b>.^1000",
        "We redefine travel.^1000",
        "Ask us anything.^1000",
        '<a class="sign-up-link">Get started</a> today!^1000',
      ],
      startDelay: 1000,
      typeSpeed: 90,
      backSpeed: 50,
      autoInsertCss: true,
      smartBackspace: true,
    });

    return () => {
      typed.destroy();
    };
  }, []);

  return (
    <div className="navbar">
      <div className="navbar-left">
        <span ref={el} className="navbar-auto-type"></span>
      </div>
      <div className="navbar-central">
        <img src={flight} alt="Flight" />
        <span className="company-name">Weir</span>
      </div>
      <div className="navbar-right">
        <button className="login-button" onClick={onLoginClick}>
          Login
        </button>
        <button className="register-button">Get Started</button>
      </div>
    </div>
  );
}

export default Navbar;
