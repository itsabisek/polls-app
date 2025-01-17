import React, { useContext, useEffect } from 'react';
import { Form, Icon, Input, Button, message } from 'antd';
import CustomLayout from '../containers/Layout'
import axios from 'axios';
import ls from 'local-storage';

const NormalLoginForm = (props) => {

    useEffect(() => {
        // console.log(props)
        if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {
            props.history.push('/user')
        }

    }, [])

    const handleSubmit = e => {
        e.preventDefault();
        const form_data = new FormData(e.target)
        props.form.validateFields((err, values) => {
            if (!err) {
                // console.log('Received values of form: ', values);
                form_data.append('username', values['username'])
                form_data.append('password', values['password'])
                axios.post('http://localhost:8000/polls/api/login/', form_data)
                    .then(response => {
                        ls.set('TOKEN', response.data['AUTH_TOKEN'])
                        ls.set('NAME', response.data['NAME'].toUpperCase())
                        message.success("Logged In Successfully")
                        if (props.location.state) {
                            if (props.location.state['referrer']) {
                                props.history.push(props.location.state['referrer'])
                            }
                        } else {
                            props.history.push('/user')
                        }

                    })
                    .catch(error => {
                        if (error.response) {
                            message.error("Failed!", 1)
                            if (error.response.status === 403) {
                                console.log(error.response)
                                props.form.setFields({
                                    password: {
                                        values: "",
                                        errors: [Error(error.response.data)]
                                    }
                                })

                            }
                            if (error.response.status === 404) {
                                message.error("Failed")
                                console.log(error.response)
                                props.history.push('/response404')

                            }
                        } else {
                            console.log(error)
                            message.error('Some error occured')
                        }

                    })

            }
        });
    };

    const { getFieldDecorator } = props.form;
    return (
        <CustomLayout selected="login">
            <Form
                onSubmit={handleSubmit}
                className="login-form"
            >
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
        </CustomLayout>
    );
}

const LoginForm = Form.create({ name: 'normal_login' })(NormalLoginForm);

export default LoginForm;