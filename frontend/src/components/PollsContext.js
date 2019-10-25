import React, { useState, createContext } from 'react'

export const PollsContext = createContext();

export const PollsProvider = (props) => {
    const [state, setState] = useState({
        polls: [],
        name: "User"
    });


    return (
        <PollsContext.Provider value={[state, setState]}>
            {props.children}
        </PollsContext.Provider>
    )
}