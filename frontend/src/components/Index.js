import React, { useContext, useEffect } from 'react'
import Axios from 'axios';
import { PollsContext } from './PollsContext';
import { QuestionList } from '../containers/QuestionList';
import CustomLayout from '../containers/Layout';

const Index = () => {

    const [state, setState] = useContext(PollsContext)

    useEffect(() => {
        Axios.get('http://localhost:8000/polls/api/all')
            .then(response => {
                setState({ ...state, polls: response.data })
            })
    }, [])

    return (
        <CustomLayout >
            <QuestionList />
        </CustomLayout>

    )
}

export default Index
