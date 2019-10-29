import React, { useContext } from 'react';
import Question from '../components/Question';
import { Layout, Divider, Input } from 'antd';
import { PollsContext } from '../components/PollsContext';
import { Button } from 'antd/lib/radio';
import { Link } from 'react-router-dom'
import Axios from 'axios';
import ls from 'local-storage'

export const QuestionList = (props) => {

    const [state, setState] = useContext(PollsContext)

    const get_info = (url, config) => {
        Axios.get(url, config)
            .then(response => {
                setState({ ...state, polls: response.data.results })
            })
            .catch(error => {
                if (error.response.status === 403) {
                    console.log(error.response)
                }

                if (error.response.status === 404) {
                    console.log(error.response)
                    props.history.push('/response404')
                }
            })
    }

    const onSearch = value => {
        if (!value) {
            console.warn("No value entered!")
        }
        else {
            let config = {}

            const url = props.referer === '/' ? `http://localhost:8000/polls/api/all?search=${value}` :
                `http://localhost:8000/polls/api${props.referer}?search=${value}`

            console.log(url)

            if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {

                config = {
                    headers: {
                        'Authorization': ls.get('TOKEN')
                    }
                }
            }
            get_info(url, config)

        }

    }

    const onChange = event => {
        let value = event.target.value
        let url = null
        let config = {}
        if (!value) {
            url = props.referer === '/' ? `http://localhost:8000/polls/api/all` :
                `http://localhost:8000/polls/api${props.referer}`

            console.log(url)

            if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {

                config = {
                    headers: {
                        'Authorization': ls.get('TOKEN')
                    }
                }
            }
        }

        else {
            if (event.target.value.length % 3 === 0) {
                url = props.referer === '/' ? `http://localhost:8000/polls/api/all?search=${value}` :
                    `http://localhost:8000/polls/api${props.referer}?search=${value}`

                console.log(url)

                if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {

                    config = {
                        headers: {
                            'Authorization': ls.get('TOKEN')
                        }
                    }
                }
            } else {
                return
            }
        }

        get_info(url, config)

    }

    return (
        <div>
            <div style={{
                width: "100 % ", display: 'flex'
            }}>
                < div>
                    <h1 style={{ margin: 0 }}>{state.polls.length}</h1>
                    <span>polls</span>
                </div>
                <Input.Search
                    // ref={(input) => { search_input = input; }}
                    style={{ width: 300, margin: "auto auto auto 30%" }}
                    placeholder="Search by question"
                    onSearch={onSearch}
                    onChange={onChange}
                    enterButton />
                <Link style={{ margin: "13px 10px 0 auto" }} to='/new'>
                    <Button >
                        Start a new poll
                    </Button>
                </Link>

            </div >

            <Divider />
            <Question data={state.polls} />
        </div >
    )
}

