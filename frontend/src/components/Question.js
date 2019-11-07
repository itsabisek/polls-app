import React from 'react';
import { List } from 'antd';
import Moment from 'react-moment';


const Question = (props) => {


    return (
        <List
            size="medium"
            dataSource={props.data}
            renderItem={item => (
                <List.Item key={item.id}>
                    <List.Item.Meta
                        title={<a href={'/detail/' + item.question_id}>{item.question_text}</a>}
                        description={
                            <p>
                                {(props.referrer === '/user/answered') ? "Voted on " : "Asked on "}
                                <Moment locale='en' format="DD MMM YYYY">
                                    {item.asked_date}
                                </Moment>
                            </p>
                        }
                    />
                    <div>{<p>{item.votes} votes </p>}</div>
                </List.Item >
            )}
        />
    )
}

export default Question;


