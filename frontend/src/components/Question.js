import React from 'react';
import { Icon, List, Button } from 'antd';


const IconText = ({ type, text }) => (
    <span>
        <Icon type={type} style={{ marginRight: 8 }} />
        {text}
    </span>
);

const Question = (props) => {
    return (
        <List
            itemLayout="vertical"
            size="large"
            pagination={{
                onChange: page => {
                    console.log(page);
                },
                pageSize: 5,

            }}
            dataSource={props.data}
            footer={
                <div>
                </div>
            }
            renderItem={item => (
                <List.Item
                    key={item.id}
                    actions={[
                        <IconText type="like-o" text={item.votes} key="list-vertical-like-o" />,
                    ]}
                >
                    <List.Item.Meta
                        title={<p>{item.question_text}</p>}
                        description={item.description}
                    />
                    Asked on {item.asked_date}
                </List.Item>
            )}
        />
    )
}

export default Question;


