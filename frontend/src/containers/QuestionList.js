import React, { Component } from 'react';
import Question from '../components/Question'
import Axios from 'axios';

const listData = [];
for (let i = 0; i < 23; i++) {
    listData.push({
        href: 'http://ant.design',
        title: `ant design part ${i}`,
        avatar: 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png',
        description:
            'Ant Design, a design language for background applications, is refined by Ant UED Team.',
        content:
            'We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.',
    });
}

export class QuestionList extends Component {
    state = {
        questions: []
    }

    componentDidMount() {
        Axios.get('http://localhost:8000/polls/api/all')
            .then(response => {
                this.setState({ questions: response.data })
                console.log(response.data)
            })
    }

    render() {
        return (
            <div>
                <Question data={this.state.questions} />
            </div>
        )
    }
}
