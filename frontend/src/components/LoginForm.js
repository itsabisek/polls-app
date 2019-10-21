import React, { useContext } from 'react';
import { Form, Icon, Input, Button } from 'antd';
import axios from 'axios';
import { PollsContext } from './PollsContext'

const NormalLoginForm = (props) => {

    const [state, setState] = useContext(PollsContext)

    const handleSubmit = e => {
        e.preventDefault();
        props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
                axios.post('http://localhost:8000/polls/api/login/', values)
                    .then(response => {
                        setState({ ...state, AUTH_TOKEN: response.data })
                    })
                    .then(() => {
                        console.log(state.AUTH_TOKEN)

                    })
                    .catch(error => {
                        if (error.response.status === 403) {
                            console.log(error.response)
                            props.form.setFields({
                                password: {
                                    values: "",
                                    errors: [Error(error.response.data)]
                                }
                            })

                        }
                    })

            }
        });
    };

    const { getFieldDecorator } = props.form;
    return (
        <Form onSubmit={handleSubmit} className="login-form">
            <Form.Item>
                {getFieldDecorator('username', {
                    rules: [{ required: true, message: 'Please input your username!' }],
                })(
                    <Input
                        name="username"
                        prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                        placeholder="Username"
                    />,
                )}
            </Form.Item>
            <Form.Item>
                {getFieldDecorator('password', {
                    rules: [{ required: true, message: 'Please input your Password!' }],
                })(
                    <Input
                        name="password"
                        prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                        type="password"
                        placeholder="Password"
                    />,
                )}
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit" className="login-form-button">
                    Log in
                    </Button>
            </Form.Item>
        </Form>
    );
}

const LoginForm = Form.create({ name: 'normal_login' })(NormalLoginForm);

export default LoginForm;