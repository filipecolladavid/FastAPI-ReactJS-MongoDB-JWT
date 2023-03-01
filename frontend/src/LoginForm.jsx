import { useState } from "react";
import { Button, Form } from "react-bootstrap";

import { BASEURL } from "./App";

const LoginForm = ({ setRegister, setLoading, setResponse, setAuth }) => {

  const [values, setValues] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [usernameNotAvail, setUsernameNotAvail] = useState(false);

  const [validated, setValidated] = useState(false);

  const onFormChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setValues({ ...values, [name]: value });
  };

  const onSubmit = (event) => {

    event.preventDefault();

    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    }
    else {
      setErrorMessage(null);
      setLoading(true);
      fetch(BASEURL + 'auth/login', {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(values)
      }).then((response => {
        if (!response.ok) {
          if (response.status === 400) {
            setUsernameNotAvail(true);
            setValidated(false);
            throw new Error("Username or password wrong");
          }
          if (response.status === 404) {
            setUsernameNotAvail(true);
            throw new Error("Not found");
          }
          else throw new Error("Something went wrong");
        }
        return response.json();
      })).then((data) => {
        setRegister(false);
        setResponse(data);
        setAuth(true);
        setValidated(true);
      }).catch((err) => {
        setErrorMessage(err.message);
      })
      setLoading(false);
    }
  }

  return (
    <Form noValidate validated={validated} onSubmit={onSubmit}>
      <h3>Login</h3>
      <Form.Group className="mb-3" controlId="formBasicUsername">
        <Form.Label>Username</Form.Label>
        <Form.Control
          placeholder="Username"
          onChange={onFormChange}
          name="username"
          required
          isInvalid={usernameNotAvail}
        />
        <Form.Control.Feedback type="invalid">{errorMessage}</Form.Control.Feedback>
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Password</Form.Label>
        <Form.Control
          type="password"
          placeholder="Password"
          onChange={onFormChange}
          name="password"
          required
          isInvalid={usernameNotAvail}
        />
        <Form.Control.Feedback type="invalid">{errorMessage}</Form.Control.Feedback>
      </Form.Group>
      <Form.Group className="mb3 d-flex justify-content-between">
        <Button onClick={() => setRegister(true)}>Don't have an account</Button>
        <Button type="submit" variant="success">Login</Button>
      </Form.Group>
      <Form.Text>{errorMessage}</Form.Text>
    </Form>
  );
}
export default LoginForm;
