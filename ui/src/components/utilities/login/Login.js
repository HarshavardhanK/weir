import * as React from "react";
import Lottie from "react-lottie";
import magician from "../../../animations/magician.json";
import google from "../../../icons/google.png";
import Dialog from "@mui/material/Dialog";
import "./Login.css";

function Login(props) {
  const defaultOptions = {
    loop: false,
    autoplay: true,
    animationData: magician,
    rendererSettings: {
      preserveAspectRatio: "xMidYMid slice",
    },
  };
  return (
    <Dialog
      open={props.isOpen}
      onClose={props.closeDialog}
      PaperProps={{ sx: { borderRadius: "16px", border: "none" } }}
    >
      <div className="login-container">
        <div className="login-title">Great things await!</div>
        <div className="login-content">
          <Lottie
            className="login-animation"
            options={defaultOptions}
            width={180}
            height={200}
          />
          <div className="login-desc">
            We care about your privacy. No data that can be traced back to you
            is stored on our servers. At <b>Weir</b> we operate on trust. Go
            ahead and login - <b>let the magic begin!</b>
          </div>
        </div>
        <div className="login-buttons">
          <button className="dialog-login-button dialog-login-button-google">
            <img src={google} height={16} width={16} />
            <span>Login with Google</span>
          </button>
          <div className="login-close" onClick={props.closeDialog}>
            close
          </div>
        </div>
      </div>
    </Dialog>
  );
}

export default Login;
