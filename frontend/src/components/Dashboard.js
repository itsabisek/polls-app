import React, { useContext, useEffect } from 'react'
import { PollsContext } from './PollsContext'
import Axios from 'axios'
import { QuestionList } from '../containers/QuestionList'
import ls from 'local-storage';
import { Redirect } from 'react-router-dom';
import UserLayout from '../containers/UserLayout';


const Dashboard = (props) => {
    const [state, setState] = useContext(PollsContext)

    useEffect(() => {
        if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {
            const config = {
                headers: {
                    'Authorization': ls.get('TOKEN')
                }
            }

            Axios.get('http://localhost:8000/polls/api/user', config)
                .then(response => {
                    setState({ ...state, polls: response.data.results })
                })
                .catch(error => {
                    if (error.response.status === 403) {
                        ls.remove('TOKEN')
                        props.history.push('/login')
                        console.log(error.response)
                    }
                })
        }
    }, [])

    return (
        <UserLayout selected="home">
            <QuestionList referer={props.history.location.pathname} />
        </UserLayout>
    )
}

export default Dashboard
