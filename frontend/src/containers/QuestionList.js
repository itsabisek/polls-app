import React, { useContext, useEffect } from 'react';
import Question from '../components/Question';
import Axios from 'axios';
import { PollsContext } from '../components/PollsContext';


export const QuestionList = () => {

    const [state, setState] = useContext(PollsContext)

    return (
        <div>
            <Question data={state.polls} />
        </div>
    )
}

