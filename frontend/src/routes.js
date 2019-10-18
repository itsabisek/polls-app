import React from 'react'
import { Route } from 'react-router-dom';
import { QuestionList } from './containers/QuestionList';

const BaseRouter = () => {
    return (
        <div>
            <Route exact path='/' component={QuestionList} />
            <Route exact path='/:question_id' component={QuestionList} />
        </div>
    )
};

export default BaseRouter;