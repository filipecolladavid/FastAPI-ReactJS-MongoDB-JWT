import { useState } from "react";
import "./App.css";
import { Container, Spinner } from "react-bootstrap";
import RegisterForm from "./RegisterForm";
import LoginForm from "./LoginForm";

export const BASEURL = "http://0.0.0.0:8000/api/";

function App() {
  const [loading, setLoading] = useState(false);
  const [register, setRegister] = useState(true);
  const [auth, setAuth] = useState(false);
  const [response, setResponse] = useState(null);

  return (
    <Container style={{ width: "30%" }}>
      {auth ? (
        <>Authenticated</>
      ) : loading ? (
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      ) : register ? (
        <RegisterForm
          setRegister={setRegister}
          setLoading={setLoading}
          setResponse={setResponse}
        />
      ) : (
        <>
          <LoginForm
            setRegister={setRegister}
            setLoading={setLoading}
            setResponse={setResponse}
            setAuth={setAuth}
          />
          {response && <>{response}</>}
        </>
      )}
    </Container>
  );
}

export default App;
