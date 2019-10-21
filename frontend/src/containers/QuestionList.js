import React, { useContext, useEffect } from 'react';
import Question from '../components/Question';
import Axios from 'axios';
import { PollsContext } from '../components/PollsContext';


export const QuestionList = () => {

    const [state, setState] = useContext(PollsContext)

    useEffect(() => {
        Axios.get('http://localhost:8000/polls/api/all')
            .then(response => {
                setState({ ...state, polls: response.data })
                console.log(response.data)
            })
    }, []);

    return (
        <div>
            <Question data={state.polls} />
        </div>
    )
}

