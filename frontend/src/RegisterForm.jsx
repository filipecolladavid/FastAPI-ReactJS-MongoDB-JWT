import { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { BASEURL } from "./App";
const RegisterForm = ({ setRegister, setLoading, setError, setSubmited }) => {

  const [values, setValues] = useState(null);

  const onFormChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setValues({ ...values, [name]: value });
  };

  const onSubmit = async (event) => {

    event.preventDefault();

    console.log(values);

    setLoading(true);
    setSubmited(true);
    let response = await fetch(BASEURL + 'auth/register', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(values)
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setError(null);
      })
      .catch(error => {
        console.error(error);
        // Handle any errors
      });
    setLoading(false);
    console.log(response);
  }

  // {
  //   "username": "string",
  //   "email": "user@example.com",
  //   "password": "string"
  // }

  return (
    <Form onSubmit={onSubmit}>
      <Form.Group className="mb-3" controlId="formBasicUsername">
        <Form.Label>Username</Form.Label>
        <Form.Control placeholder="Username" onChange={onFormChange} name="username" />
      </Form.Group>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Email</Form.Label>
        <Form.Control placeholder="Email" onChange={onFormChange} name="email" />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Password" onChange={onFormChange} name="password" />
      </Form.Group>
      <Form.Group className="mb3 d-flex justify-content-between">
        <Button onClick={() => setRegister(false)}>Already Registered</Button>
        <Button type="submit" variant="success">Register</Button>
      </Form.Group>
    </Form>
  );
}

export default RegisterForm;