import React from 'react';
import { Layout, Menu, Button, Icon, Typography } from 'antd';
import { Link } from 'react-router-dom';
import ls from 'local-storage';
const { Title } = Typography;
const { Header, Content, Footer } = Layout;


const UserLayout = (props) => {

    return (
        <Layout className="layout">
            <Header style={{ position: 'fixed', zIndex: 2, width: '100%' }}>
                <Link to='/user'>
                    <Title level={1} style={{ color: "#fff", margin: "8px 8px" }}>
                        WELCOME {(ls.get('NAME') != null && ls.get('NAME').length != 0) ? ls.get('NAME') : "USER"}</Title>
                </Link>
            </Header>
            <Layout>
                <Menu
                    mode="horizontal"
                    selectedKeys={[props.selected]}
                    style={{ position: 'fixed', zIndex: 1, width: '100%', 'marginTop': '64px' }}
                >
                    <Menu.Item key="home">
                        <Link to='/user'>
                            <Icon type="home" />
                            HOME
                        </Link>
                    </Menu.Item>
                    <Menu.Item key="asked">
                        <Link to='/user/asked'>
                            <Icon type="question" />
                            CREATED
                        </Link>
                    </Menu.Item>
                    <Menu.Item key="answered" >
                        <Link to='/user/answered'>
                            <Icon type="check-circle" />
                            VOTED
                        </Link>
                    </Menu.Item>
                    <Menu.Item key="logout" >
                        <Link to='/logout'>
                            <Icon type="logout" />
                            LOG OUT
                        </Link>
                    </Menu.Item>
                </Menu>
                <Content style={{ padding: '0 50px', marginTop: '120px' }}>
                    <div style={{ background: '#fff', padding: 24, minHeight: 280 }}>
                        {props.children}
                    </div>

                </Content>
            </Layout>

            <Footer style={{ textAlign: 'center' }}>Ant Design ©2018 Created by Ant UED</Footer>
        </Layout >
    )
}

export default UserLayout


