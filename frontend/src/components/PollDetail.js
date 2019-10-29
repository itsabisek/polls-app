import React, { useEffect, useState } from 'react'
import Axios from 'axios'
import ls from 'local-storage';
import UserLayout from '../containers/UserLayout'
import { Button, Card, Form, Radio, Progress, Popover } from 'antd';
import Moment from 'react-moment';

const PollDetailForm = (props) => {

    const [state, setState] = useState({
        question_id: "",
        question_text: "",
        asked_date: "",
        choice_1: {},
        choice_2: {},
        total_votes: 0,
        disableVote: true,
        disableResult: true
    })

    useEffect(() => {
        const question_id = props.match.params.question_id
        let config = {}
        if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {
            config = {
                headers: {
                    'Authorization': ls.get('TOKEN')
                }
            }
        }

        Axios.get(`http://localhost:8000/polls/api/detail/${question_id}`, config)
            .then(response => {
                console.log(response.data)
                const data = response.data
                if (!data.choices[0].hasOwnProperty('choice_votes') || !data.choices[1].hasOwnProperty('choice_votes')) {
                    setState({
                        disableResult: true,
                        disableVote: false,
                        question_id: data.question_id,
                        question_text: data.question_text,
                        asked_date: data.asked_date,
                        choice_1: data.choices[0],
                        choice_2: data.choices[1],
                        total_votes: data.votes
                    })
                } else {
                    setState({
                        ...state,
                        disableResult: false,
                        question_id: data.question_id,
                        question_text: data.question_text,
                        asked_date: data.asked_date,
                        choice_1: data.choices[0],
                        choice_2: data.choices[1],
                        total_votes: data.votes
                    })
                }
                console.log(state)
            })
            .catch(error => {
                if (error.response.status === 403) {
                    console.log(error.response)
                    ls.remove('TOKEN')
                    props.history.push('/login')
                }
                if (error.response.status === 404) {
                    props.history.push('/404')
                }
            })
    }, [])

    const handleSubmit = e => {
        e.preventDefault();
        props.form.validateFields((err, values) => {
            if (!err) {
                if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {
                    const config = {
                        headers: {
                            'Authorization': ls.get('TOKEN')
                        }
                    }

                    Axios.post(`http://localhost:8000/polls/api/vote/${props.match.params.question_id}/`, values, config)
                        .then(response => {
                            const data = response.data
                            setState({
                                disableResult: false,
                                disableVote: true,
                                question_id: data.question_id,
                                question_text: data.question_text,
                                asked_date: data.asked_date,
                                choice_1: data.choices[0],
                                choice_2: data.choices[1],
                                total_votes: data.votes

                            })
                            console.log(data.choices[0].choice_votes)
                        })
                        .catch(error => {
                            if (error.response.status === 403) {
                                console.log(error.response)
                                ls.remove('TOKEN')
                                props.history.push('/login')
                            }
                            if (error.response.status === 404) {
                                console.log(error.response)
                                props.history.push('/404')
                            }

                        })
                }
            }
        });
    }

    const { getFieldDecorator } = props.form

    return (
        <UserLayout selected="">
            <Card title={state.question_text}>
                <p
                    style={{
                        fontSize: 14,
                        color: 'rgba(0, 0, 0, 0.85)',
                        marginBottom: 16,
                        fontWeight: 500,
                        display: "flex"
                    }}
                >
                    <span style={{ margin: '0 auto 0 0', fontSize: "9pt", fontStyle: 'italic' }}>
                        Asked on &nbsp;
                        <Moment locale='en' format="DD MMM YYYY">
                            {state.asked_date}
                        </Moment>

                    </span>

                    <span style={{ margin: '0 0 0 auto', fontSize: "9pt", fontStyle: 'italic' }}>
                        {state.total_votes}
                        {state.total_votes > 1 ? ' people have voted' : ' person have voted'}
                    </span>
                </p>
                <Form onSubmit={handleSubmit} className="vote-form" style={{ width: "100 %" }}>
                    <Form.Item>
                        {getFieldDecorator('choice', {
                            rules: [{ required: true, message: 'Please select atleast 1 choice!' }]
                        })(
                            <Radio.Group >
                                <Radio
                                    value={state.choice_1.id}
                                    disabled={state.disableVote}
                                >
                                    {state.choice_1.choice_text}
                                </Radio>
                                <br />
                                <Radio
                                    value={state.choice_2.id}
                                    disabled={state.disableVote}
                                >
                                    {state.choice_2.choice_text}
                                </Radio>
                            </Radio.Group>,
                        )}
                    </Form.Item>
                    <Form.Item>
                        <Button
                            type="primary"
                            htmlType="submit"
                            className="login-form-button"
                            disabled={state.disableVote}
                        >
                            VOTE
                        </Button>
                    </Form.Item>
                </Form>
                <Popover
                    placement='topLeft'
                    content={<div><p>First Choice: {state.choice_1.choice_votes} votes</p>
                        <p>Second Choice: {state.choice_2.choice_votes} votes</p></div>}
                    title="Results"
                    trigger="hover"
                    visible={!state.disableResult}>
                    <Progress
                        status='exception'
                        size='small'
                        percent={state.disableResult ? 0 : 100}
                        successPercent={state.disableResult ? 0 : (state.choice_1.choice_votes / state.total_votes) * 100}
                        showInfo={false}
                    />
                </Popover>

            </Card>
        </UserLayout >

    )
}

const PollDetail = Form.create({ name: 'poll_vote' })(PollDetailForm)
export default PollDetail
