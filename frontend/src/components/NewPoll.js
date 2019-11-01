import React from 'react';
import { Form, Icon, Input, Button, message } from 'antd';
import axios from 'axios';
import UserLayout from '../containers/UserLayout'
import ls from 'local-storage';

const NewPollForm = (props) => {

    const handleSubmit = e => {
        e.preventDefault();
        props.form.validateFields((err, values) => {
            if (!err) {
                // console.log('Received values of form: ', values);
                if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {
                    const config = {
                        headers: {
                            'Authorization': ls.get('TOKEN')
                        }
                    }
                    axios.post('http://localhost:8000/polls/api/user/new/', values, config)
                        .then(response => {
                            const question_id = response.data['question_id']
                            props.history.push(`/detail/${question_id}`)
                        })
                        .catch(error => {
                            if (error.response) {
                                if (error.response.status === 403) {
                                    console.log(error.response)
                                    ls.remove('TOKEN')
                                    props.history.push('/login')
                                }
                                if (error.response.status === 404) {
                                    console.log(error.response)
                                    props.form.setFields({
                                        question: {
                                            value: values.question,
                                            errors: [Error("The question could not be created. Try Again")]
                                        },
                                        choice_1: {
                                            value: ""
                                        },
                                        choice_2: {
                                            value: ""
                                        }
                                    })
                                }
                                else {
                                    console.log(error.response)
                                    message.error("Some error has occured")
                                }
                            } else {
                                console.log(error)
                                message.error("Some error has occured")
                            }

                        })
                }
            }
        });
    };

    const { getFieldDecorator } = props.form;
    return (
        <UserLayout>
            <Form onSubmit={handleSubmit} className="login-form">
                <Form.Item>
                    {getFieldDecorator('question', {
                        rules: [{ required: true, message: 'Please ask a question!' },
                        { min: 10, message: "The question should be atleast 10 characters" }],
                    })(
                        <Input
                            prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                            placeholder="Question"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('choice_1', {
                        rules: [{ required: true, message: 'Please enter a choice!' },
                        { min: 2, message: "The choice should be atleast 2 characters" },
                        { max: 100, message: "The choice can be atmost 100 characters" }],
                    })(
                        <Input
                            prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                            placeholder="1st Choice"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('choice_2', {
                        rules: [{ required: true, message: 'Please enter a choice!' },
                        { min: 2, message: 'The choice should be atleast 2 characters' },
                        { max: 100, message: "The choice can be atmost 100 characters" }],
                    })(
                        <Input
                            prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                            placeholder="2nd Choice"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit" className="login-form-button">
                        Create Poll
                    </Button>
                </Form.Item>
            </Form>
        </UserLayout>
    );
}

const NewPoll = Form.create({ name: 'new_poll' })(NewPollForm);

export default NewPoll;