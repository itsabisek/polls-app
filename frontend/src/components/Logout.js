import React, { useEffect, useContext } from 'react'
import ls from 'local-storage';
import { Redirect } from 'react-router-dom';
import { message } from 'antd';

const Logout = () => {

    useEffect(() => {
        if (ls.get('TOKEN') != null && ls.get('TOKEN').length != 0) {
            ls.remove('TOKEN')

            if (ls.get('NAME') != null && ls.get('NAME').length != 0) {
                ls.remove('NAME')
            }
            message.success("Logged out successfully!")
        }
    }, [])

    return (
        <Redirect to='/' />
    )
}

export default Logout
