import React, { useState, createContext } from 'react'

export const PollsContext = createContext();

export const PollsProvider = (props) => {
    const [state, setState] = useState({
        polls: [],
        total_polls: 0,
        next_url: "",
        previous_url: "",
        limit: 10,
        offset: 0,
        current_page: 1
    });


    return (
        <PollsContext.Provider value={[state, setState]}>
            {props.children}
        </PollsContext.Provider>
    )
}