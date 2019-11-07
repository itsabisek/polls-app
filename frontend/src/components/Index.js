import React, { useContext, useEffect } from 'react'
import Axios from 'axios';
import { PollsContext } from './PollsContext';
import { QuestionList } from '../containers/QuestionList';
import CustomLayout from '../containers/Layout';
import { message } from 'antd';

const Index = (props, a) => {
    console.log(a);
    const [state, setState] = useContext(PollsContext)

    useEffect(() => {
        Axios.get('http://localhost:8000/polls/api/all?limit=10&offset=0')
            .then(response => {
                console.log(response.data)
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
                    if (error.response.status == 403) {
                        message.error("Some error has occured!")
                        console.log(error.response)
                    }
                    if (error.response.status == 404) {
                        console.log(error.response)
                        props.history.push('/response404')
                    }
                    else {
                        console.log(error.response)
                        message.error("Some error has occured")
                    }
                } else {
                    console.log(error)
                    message.error("Some error has occured.")
                }

            })
    }, [])


    return (
        <CustomLayout >
            <QuestionList referrer={props.history.location.pathname} />
        </CustomLayout>

    )
}

export default Index
