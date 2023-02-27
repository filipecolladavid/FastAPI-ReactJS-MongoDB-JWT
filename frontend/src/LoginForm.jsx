import { Button, Form } from "react-bootstrap";

const LoginForm = ({ setRegister, setLoading, setError }) => {
  return (
    <Form>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Username</Form.Label>
        <Form.Control placeholder="Username" />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Password" />
      </Form.Group>
      <Form.Group className="d-flex justify-content-between">
        <Button onClick={() => setRegister(true)}>Don't have an account</Button>
        <Button type="submit" variant="success">Login</Button>
      </Form.Group>
    </Form>
  );
}

export default LoginForm;