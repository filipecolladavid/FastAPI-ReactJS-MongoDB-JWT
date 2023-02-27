import { useState } from "react";
import "./App.css";
import { Container, Spinner } from "react-bootstrap";
import RegisterForm from "./RegisterForm";
import LoginForm from "./LoginForm";

export const BASEURL = "http://0.0.0.0:8000/api/";

function App() {
  const [register, setRegister] = useState(false);
  const [loading, setLoading] = useState(false);
  const [submited, setSubmited] = useState(false);
  const [error, setError] = useState(null);

  return (
    <Container style={{ width: "20%" }}>
      {loading ? (
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      ) : submited ? (
        !error ? (
          <>Valid</>
        ) : (
          <>Invalid</>
        )
      ) : register ? (
        <RegisterForm
          setRegister={setRegister}
          setLoading={setLoading}
          setError={setError}
          setSubmited={setSubmited}
        />
      ) : (
        <LoginForm
          setRegister={setRegister}
          setLoading={setLoading}
          setError={setError}
        />
      )}
    </Container>
  );
}

export default App;
