import { Route, Redirect } from 'react-router-dom';
import React from 'react';
import ls from 'local-storage'


const ProtectedRoute = ({ component: Component, ...rest }) => {

    return (
        <Route
            {...rest}
            render={(props) => {
                // console.log(`Token is ${ls.get('TOKEN')}`)
                // console.log(rest.location['pathname'])
                return ((ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) ?
                    <Component {...props} /> :
                    (rest.path === '/detail/:question_id' || rest.path === '/new') ?
                        < Redirect to={{ pathname: '/login', state: { referrer: rest.location['pathname'] } }} /> :
                        <Redirect to='/login' />
                )
            }
            }
        />
    )
}


export default ProtectedRoute