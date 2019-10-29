import React, { useEffect, useContext } from 'react'
import ls from 'local-storage';
import { Redirect } from 'react-router-dom';
import { PollsContext } from './PollsContext';

const Logout = () => {

    useEffect(() => {
        if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {
            ls.remove('TOKEN')
        }
    }, [])

    return (
        <Redirect to='/' />
    )
}

export default Logout
