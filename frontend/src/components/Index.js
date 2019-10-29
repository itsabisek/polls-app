import React, { useContext, useEffect } from 'react'
import Axios from 'axios';
import { PollsContext } from './PollsContext';
import { QuestionList } from '../containers/QuestionList';
import CustomLayout from '../containers/Layout';

const Index = (props) => {

    const [state, setState] = useContext(PollsContext)

    useEffect(() => {
        Axios.get('http://localhost:8000/polls/api/all')
            .then(response => {
                setState({ ...state, polls: response.data.results })
            })
            .catch(error => {
                if (error.response.status == 403) {
                    console.log(error.response)
                }
                if (error.response.status == 404) {
                    console.log(error.response)
                    props.history.push('/response404')
                }
            })
    }, [])


    return (
        <CustomLayout >
            <QuestionList referer={props.history.location.pathname} />
        </CustomLayout>

    )
}

export default Index
