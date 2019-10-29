import { Route, Redirect } from 'react-router-dom';
import React, { Component, useContext } from 'react';
import { PollsContext } from './PollsContext';
import ls from 'local-storage'


const ProtectedRoute = ({ component: Component, ...rest }) => {

    const [state, setState] = useContext(PollsContext)

    return (
        <Route
            {...rest}
            render={(props) => {
                console.log(`Token is ${ls.get('TOKEN')}`)

                return ((ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) ?
                    <Component {...props} /> :
                    <Redirect to='/login' />
                )
            }}
        />
    )
}

export default ProtectedRoute