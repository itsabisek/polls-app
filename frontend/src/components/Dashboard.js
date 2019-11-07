import React, { useContext, useEffect } from 'react'
import { PollsContext } from './PollsContext'
import Axios from 'axios'
import { QuestionList } from '../containers/QuestionList'
import ls from 'local-storage';
import { Redirect } from 'react-router-dom';
import UserLayout from '../containers/UserLayout';
import { message } from 'antd';


const Dashboard = (props) => {
    const [state, setState] = useContext(PollsContext)

    useEffect(() => {
        if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {
            const config = {
                headers: {
                    'Authorization': ls.get('TOKEN')
                }
            }

            Axios.get('http://localhost:8000/polls/api/user?offset=0&limit=10', config)
                .then(response => {
                    setState({
                        ...state,
                        polls: response.data.results,
                        total_polls: response.data.count,
                        next_url: response.data.next,
                        previous_url: response.data.previous
                    })
                })
                .catch(error => {
                    if (error.response) {
                        if (error.response.status === 403) {
                            ls.remove('TOKEN')
                            props.history.push('/login')
                            console.log(error.response)
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
                        message.error("Some error has occured")
                    }

                })
        }
    }, [])

    return (
        <UserLayout selected="home">
            <QuestionList referrer={props.history.location.pathname} />
        </UserLayout>
    )
}

export default Dashboard
