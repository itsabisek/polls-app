import React from 'react'
import { Layout, Menu, Icon } from 'antd';
import { Link } from 'react-router-dom';
import Title from 'antd/lib/typography/Title';

const { Header, Content, Footer, Sider } = Layout;

const CustomLayout = (props) => {


    return (
        <Layout className="layout">
            <Header style={{ position: 'fixed', zIndex: 2, width: '100%' }}>
                <Link to='/'>
                    <Title level={1} style={{ color: "#fff", margin: "8px 8px" }}>WELCOME</Title>
                </Link>
            </Header>
            <Layout>
                <Menu
                    mode="horizontal"
                    style={{ position: 'fixed', zIndex: 1, width: '100%', 'marginTop': '64px' }}
                    selectedKeys={[props.selected]}
                >
                    <Menu.Item key="login">
                        <Link to='/login'>
                            <Icon type="login" />
                            LOGIN
                        </Link>
                    </Menu.Item>
                    <Menu.Item key="signup" >
                        <Link to='/signup'>
                            <Icon type="form" />
                            SIGN UP
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
        </Layout>
    )
}

export default CustomLayout


