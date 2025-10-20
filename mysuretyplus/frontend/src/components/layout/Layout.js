import React, { useState } from 'react';
import { Layout as AntLayout, Menu, Button, Avatar, Dropdown, Space, Typography } from 'antd';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  DashboardOutlined,
  FileTextOutlined,
  BarChartOutlined,
  UserOutlined,
  LogoutOutlined,
  SettingOutlined
} from '@ant-design/icons';
import { useAuth } from '../../contexts/AuthContext';
import styled from 'styled-components';

import Dashboard from '../dashboard/Dashboard';
import SimulationForm from '../dashboard/SimulationForm';
import SimulationResults from '../dashboard/SimulationResults';
import RiskCalculator from '../dashboard/RiskCalculator';
import DataPreview from '../dashboard/DataPreview';
import MethodComparison from '../dashboard/MethodComparison';
import SimulationHistory from '../dashboard/SimulationHistory';

const { Header, Sider, Content } = AntLayout;
const { Title } = Typography;

const StyledLayout = styled(AntLayout)`
  min-height: 100vh;
`;

const StyledHeader = styled(Header)`
  padding: 0 24px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
`;

const StyledSider = styled(Sider)`
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: 999;
  
  .ant-layout-sider-children {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
`;

const FixedLogo = styled.div`
  position: sticky;
  top: 0;
  z-index: 1001;
  background: #1890ff;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  font-weight: bold;
  flex-shrink: 0;
`;

const ScrollableMenu = styled.div`
  flex: 1;
  overflow-y: auto;
  padding-top: 0;
`;

const Logo = styled.div`
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1890ff;
  color: white;
  font-size: 18px;
  font-weight: bold;
`;



const ScrollingText = styled.div`
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(90deg, #1890ff, #722ed1);
  color: white;
  padding: 8px 0;
  font-size: 14px;
  font-style: italic;
  text-align: center;
  z-index: 1000;
  overflow: hidden;
  white-space: nowrap;
  
  .scrolling-content {
    display: inline-block;
    animation: scroll 60s linear infinite;
  }
  
  @keyframes scroll {
    0% {
      transform: translateX(100%);
    }
    100% {
      transform: translateX(-100%);
    }
  }
`;

const StyledContent = styled(Content)`
  margin: 24px;
  padding: 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  min-height: calc(100vh - 112px);
  margin-bottom: 40px; /* Espace pour le texte défilant */
`;

const Layout = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [activeView, setActiveView] = useState('dashboard');
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  const handleMenuClick = ({ key }) => {
    setActiveView(key);
  };

  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'Profil',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Paramètres',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Déconnexion',
      onClick: handleLogout,
    },
  ];

  const menuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: 'Tableau de bord',
    },
    {
      key: 'simulations',
      icon: <FileTextOutlined />,
      label: 'Simulations',
    },
    {
      key: 'analytics',
      icon: <BarChartOutlined />,
      label: 'Analyses',
    },
  ];

  const renderContent = () => {
    switch (activeView) {
      case 'dashboard':
        return <Dashboard />;
      case 'simulations':
        return (
          <div>
            <h1>🚀 Section Simulations</h1>
            <p>Configuration et lancement des simulations Monte Carlo et Bootstrap</p>
            <SimulationForm />
            <div style={{ marginTop: '32px' }}>
              <MethodComparison />
            </div>
            <div style={{ marginTop: '32px' }}>
              <SimulationHistory />
            </div>
          </div>
        );
      case 'analytics':
        return (
          <div>
            <h1>📊 Section Analyses</h1>
            <p>Résultats des simulations et analyse des risques</p>
            <SimulationResults />
            <RiskCalculator />
          </div>
        );
      default:
        return <Dashboard />;
    }
  };

  return (
    <StyledLayout>
      <StyledSider trigger={null} collapsible collapsed={collapsed}>
        <FixedLogo>
          {collapsed ? (
            <span>M</span>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>My Surety +</span>
            </div>
          )}
        </FixedLogo>
        <ScrollableMenu>
          <Menu
            theme="dark"
            mode="inline"
            selectedKeys={[activeView]}
            items={menuItems}
            onClick={handleMenuClick}
            style={{ border: 'none' }}
          />
        </ScrollableMenu>
      </StyledSider>
      
      <AntLayout>
        <StyledHeader>
          <Space>
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
              style={{
                fontSize: '16px',
                width: 64,
                height: 64,
              }}
            />
            <img 
              src="/images/epsilon-ai-logo.jpg" 
              alt="EPSILON AI" 
              style={{ 
                height: '40px', 
                width: 'auto',
                objectFit: 'contain'
              }} 
            />
          </Space>
          
          <Space>
            <Dropdown
              menu={{ items: userMenuItems }}
              placement="bottomRight"
              arrow
            >
              <Space style={{ cursor: 'pointer' }}>
                <Avatar icon={<UserOutlined />} />
                <span>{user?.username}</span>
              </Space>
            </Dropdown>
          </Space>
        </StyledHeader>
        
        <StyledContent>
          {renderContent()}
        </StyledContent>
      </AntLayout>
      
      <ScrollingText>
        <div className="scrolling-content">
          Une intelligence qui pour un instant donné, connaîtrait toutes les forces dont la nature est animée, et la situation respective des êtres qui la composent, si d'ailleurs elle était assez vaste pour soumettre ces données à l'analyse, embrasserait dans la même formule, les mouvements des plus grands corps de l'univers et ceux du plus léger atome: rien ne serait incertain pour elle, et l'avenir comme le passé serait présent à ses yeux. - Pierre - Simon LAPLACE
        </div>
      </ScrollingText>
    </StyledLayout>
  );
};

export default Layout;



