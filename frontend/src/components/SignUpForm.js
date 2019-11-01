import React, { useContext } from 'react';
import { Form, Icon, Input, Button, message } from 'antd';
import axios from 'axios';
import ls from 'local-storage';
import CustomLayout from '../containers/Layout'

const NormalSignUpForm = (props) => {

    const handleSubmit = e => {
        e.preventDefault();
        props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
                const password = values.password
                const confirm = values.confirm
                if (password !== confirm) {
                    props.form.setFields({
                        password: {
                            value: "",
                            errors: [new Error("Passwords don't match")],
                        },
                        confirm: {
                            value: "",
                            errors: [new Error("Passwords don't match")],
                        }
                    })
                    return
                }
                axios.post('http://localhost:8000/polls/api/register/', values)
                    .then(response => {
                        ls.set('TOKEN', response.data['AUTH_TOKEN'])
                        ls.set('NAME', response.data['NAME'].toUpperCase())
                        message.success("You are now Registered!")
                        props.history.push('/user')
                    })
                    .catch(error => {
                        if (error.response) {
                            if (error.response.status == 403) {
                                message.error("Failed!", 1)
                                console.log(error.response)
                                props.form.setFields({
                                    username: {
                                        value: values.username,
                                        errors: [Error(error.response.data)]
                                    },
                                    password: {
                                        value: ""
                                    },
                                    confirm: {
                                        value: ""
                                    }
                                })
                            }
                            if (error.response.status == 404) {
                                message.error("Failed!")
                                console.log(error.response)
                                props.history.push('/response404')
                            }
                        } else {
                            console.log(error)
                            message.error("Some Error Occured!")
                        }

                    })

            }
        });
    };

    const { getFieldDecorator } = props.form;
    return (
        <CustomLayout selected='signup'>
            <Form onSubmit={handleSubmit} className="login-form">
                <Form.Item>
                    {getFieldDecorator('name', {
                        rules: [{ required: true, message: 'Please input your name!' }],
                    })(
                        <Input
                            prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                            placeholder="Name"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('username', {
                        rules: [{ required: true, message: 'Please input your username!' },
                        { min: 4, message: "The username should be atleast 4 characters" }],
                    })(
                        <Input
                            prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                            placeholder="Username"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('password', {
                        rules: [{ required: true, message: 'Please input your Password!' },
                        { min: 6, message: 'Password should be atleast 6 characters' }],
                    })(
                        <Input
                            prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                            type="password"
                            placeholder="Password"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('confirm', {
                        rules: [{ required: true, message: 'Please confirm your Password!' }],
                    })(
                        <Input
                            prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                            type="password"
                            placeholder="Confirm Password"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit" className="login-form-button">
                        Sign Up
                    </Button>
                </Form.Item>
            </Form>
        </CustomLayout>
    );
}

const SignUpForm = Form.create({ name: 'normal_signup' })(NormalSignUpForm);

export default SignUpForm;