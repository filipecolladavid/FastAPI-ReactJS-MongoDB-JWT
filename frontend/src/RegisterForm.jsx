import { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { BASEURL } from "./App";
const RegisterForm = ({ setRegister, setLoading, setResponse }) => {

  const [values, setValues] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [mailInvalid, setMailInvalid] = useState(false);
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
      setMailInvalid(false);
      setErrorMessage(null);
      setLoading(true);
      fetch(BASEURL + 'auth/register', {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(values)
      }).then((response => {
        if (!response.ok) {
          if (response.status === 400) {
            setMailInvalid(true);
            setValidated(false);
            throw new Error("Invalid Email");
          }
          if (response.status === 409) {
            setUsernameNotAvail(true);
            throw new Error("Username or email already registred");
          }
          else throw new Error("Something went wrong");
        }
        return response.json();
      })).then((data) => {
        setRegister(false);
        setResponse(data.username + " registred with success");
      }).catch((err) => {
        setErrorMessage(err.message);
      })
      setLoading(false);
    }
  }

  return (
    <Form noValidate validated={validated} onSubmit={onSubmit}>
      <h3>Register</h3>
      <Form.Group className="mb-3" controlId="formBasicUsername">
        <Form.Label>Username</Form.Label>
        <Form.Control
          placeholder="Username"
          onChange={onFormChange}
          name="username"
          required
          isInvalid={mailInvalid || usernameNotAvail}
        />
        <Form.Control.Feedback type="invalid">Invalid username</Form.Control.Feedback>
      </Form.Group>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Email</Form.Label>
        <Form.Control
          placeholder="Email"
          onChange={onFormChange}
          name="email"
          required
          isInvalid={mailInvalid || usernameNotAvail}
        />
        <Form.Control.Feedback type="invalid">Invalid email</Form.Control.Feedback>
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Password" onChange={onFormChange} name="password" required />
      </Form.Group>
      <Form.Group className="mb3 d-flex justify-content-between">
        <Button onClick={() => setRegister(false)}>Already Registered</Button>
        <Button type="submit" variant="success">Register</Button>
      </Form.Group>
      <Form.Text>{errorMessage}</Form.Text>
    </Form>
  );
}

export default RegisterForm;
