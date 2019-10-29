import React from 'react';
import { Icon, List, Button } from 'antd';
import Moment from 'react-moment';

const IconText = ({ type, text }) => (
    <span>
        <Icon type={type} style={{ marginRight: 8 }} />
        {text}
    </span>
);

const Question = (props) => {
    return (
        <List
            size="medium"
            pagination={{
                onChange: page => {
                    console.log(page);
                },
                pageSize: 10,

            }}
            dataSource={props.data}
            renderItem={item => (
                <List.Item key={item.id}>
                    <List.Item.Meta
                        title={<a href={'/detail/' + item.question_id}>{item.question_text}</a>}
                        description={<p>Asked on &nbsp;
                            <Moment locale='en' format="DD MMM YYYY">
                                {item.asked_date}
                            </Moment>
                        </p>}
                    />
                    <div>{<p>{item.votes} votes </p>}</div>
                </List.Item >
            )}
        />
    )
}

export default Question;


