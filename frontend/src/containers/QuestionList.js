import React, { useContext } from 'react';
import Question from '../components/Question';
import { Layout, Divider } from 'antd';
import { PollsContext } from '../components/PollsContext';
import { Button } from 'antd/lib/radio';
import { Link } from 'react-router-dom'
const { Header } = Layout;

export const QuestionList = () => {

    const [state, setState] = useContext(PollsContext)

    return (
        <div>
            <div style={{
                width: "100 % ", display: 'flex'
            }}>
                < div>
                    <h1 style={{ margin: 0 }}>{state.polls.length}</h1>
                    <span>polls</span>
                </div>
                <Link style={{ margin: "13px 50px 0 auto" }} to='/new'>
                    <Button >
                        Start a new poll
                    </Button>
                </Link>

            </div >

            <Divider />
            <Question data={state.polls} />
        </div >
    )
}

