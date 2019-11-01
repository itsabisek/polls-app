import React, { useContext } from 'react';
import Question from '../components/Question';
import { Divider, Input, Pagination, message } from 'antd';
import { PollsContext } from '../components/PollsContext';
import { Button } from 'antd/lib/radio';
import { Link } from 'react-router-dom'
import Axios from 'axios';
import ls from 'local-storage'

export const QuestionList = (props, params) => {

    const [state, setState] = useContext(PollsContext)
    let search_input = null

    const get_info = (url, config, current_page) => {
        Axios.get(url, config)
            .then(response => {
                // console.log(response)
                setState({
                    ...state,
                    polls: response.data.results,
                    total_polls: response.data.count,
                    next_url: response.data.next,
                    previous_url: response.data.previous,
                    current_page: current_page
                })

            })
            .catch(error => {
                if (error.response) {
                    if (error.response.status === 403) {
                        console.log(error.response)
                        message.error("Some error has occured")
                    }

                    if (error.response.status === 404) {
                        console.log(error.response)
                        props.history.push('/response404')
                    }
                    else {
                        console.log(error.response)
                        message.error("Some error has occured")
                    }
                } else {
                    console.log(error)
                    message.error("Some error occured")
                }

            })
    }

    const onSearch = value => {
        if (!value) {
            console.warn("No value entered!")
        }
        else {
            let config = {}

            const url = props.referrer === '/' ? `http://localhost:8000/polls/api/all?search=${value}&limit=10&offset=0` :
                `http://localhost:8000/polls/api${props.referrer}?search=${value}&limit=10&offset=0`

            // console.log(url)

            if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {

                config = {
                    headers: {
                        'Authorization': ls.get('TOKEN')
                    }
                }
            }
            get_info(url, config, 1)

        }

    }

    const on_search_change = event => {
        let value = event.target.value
        let url = null
        let config = {}
        if (!value) {
            on_page_change(1)
            return
        }

        else {
            if (event.target.value.length % 3 === 0) {
                url = props.referrer === '/' ? `http://localhost:8000/polls/api/all?search=${value}` :
                    `http://localhost:8000/polls/api${props.referrer}?search=${value}&limit=10&offset=0`

                // console.log(url)

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

        get_info(url, config, 1)

    }

    const on_page_change = page => {
        // console.log(page)
        let query_string = ""
        let config = {}
        const limit = 10
        const offset = (page - 1) * limit

        if (search_input.input.input.value) {
            query_string += `search=${search_input.input.input.value}&`
        }

        query_string += `limit=${limit}&offset=${offset}`
        const url = props.referrer === '/' ? `http://localhost:8000/polls/api/all?${query_string}` :
            `http://localhost:8000/polls/api${props.referrer}?${query_string}`

        if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {

            config = {
                headers: {
                    'Authorization': ls.get('TOKEN')
                }
            }
        }

        get_info(url, config, page)
    }

    return (
        <div>
            <div style={{
                width: "100 % ", display: 'flex'
            }}>
                < div>
                    <h1 style={{ margin: 0 }}>{state.total_polls}</h1>
                    <span>polls</span>
                </div>
                <div style={{ width: 300, margin: "auto auto auto 30%" }}>
                    <Input.Search
                        ref={(node) => { search_input = node; }}
                        placeholder="Search by question"
                        onSearch={onSearch}
                        onChange={on_search_change}
                        enterButton />
                </div>

                <Link style={{ margin: "13px 10px 0 auto" }} to='/new'>
                    <Button >
                        Start a new poll
                    </Button>
                </Link>

            </div >

            <Divider />
            <Question data={state.polls} referrer={props.referrer} />
            <Pagination
                defaultCurrent={1}
                current={state.current_page}
                defaultPageSize={10}
                onChange={on_page_change}
                total={state.total_polls}
            />
        </div >
    )
}

