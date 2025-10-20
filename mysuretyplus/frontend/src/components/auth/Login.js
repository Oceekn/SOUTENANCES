import React, { useState } from 'react';
import { Form, Input, Button, Card, Typography, message, Space } from 'antd';
import { UserOutlined, LockOutlined, LoginOutlined } from '@ant-design/icons';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import styled from 'styled-components';

const { Title, Text } = Typography;

const LoginContainer = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const LoginCard = styled(Card)`
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  
  .ant-card-body {
    padding: 40px;
  }
`;

const StyledTitle = styled(Title)`
  text-align: center;
  margin-bottom: 30px !important;
  color: #1890ff;
`;

const Login = () => {
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);
    
    try {
      const result = await login(values.username, values.password);
      
      if (result.success) {
        message.success('Connexion réussie !');
        navigate('/dashboard');
      } else {
        message.error(result.error);
      }
    } catch (error) {
      message.error('Erreur lors de la connexion');
    } finally {
      setLoading(false);
    }
  };

  return (
    <LoginContainer>
      <LoginCard>
        <StyledTitle level={2}>
          <LoginOutlined /> Connexion
        </StyledTitle>
        
        <Form
          name="login"
          onFinish={onFinish}
          autoComplete="off"
          layout="vertical"
          size="large"
        >
          <Form.Item
            name="username"
            label="Nom d'utilisateur"
            rules={[
              {
                required: true,
                message: 'Veuillez saisir votre nom d\'utilisateur !',
              },
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="Nom d'utilisateur"
            />
          </Form.Item>

          <Form.Item
            name="password"
            label="Mot de passe"
            rules={[
              {
                required: true,
                message: 'Veuillez saisir votre mot de passe !',
              },
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Mot de passe"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
              size="large"
              style={{
                height: '48px',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '600'
              }}
            >
              Se connecter
            </Button>
          </Form.Item>
        </Form>

        <Space direction="vertical" style={{ width: '100%', textAlign: 'center' }}>
          <Text>
            <Link to="/forgot-password" style={{ color: '#1890ff', fontWeight: '600' }}>
              Mot de passe oublié ?
            </Link>
          </Text>
          <Text>
            Pas encore de compte ?{' '}
            <Link to="/register" style={{ color: '#1890ff', fontWeight: '600' }}>
              S'inscrire
            </Link>
          </Text>
        </Space>
      </LoginCard>
    </LoginContainer>
  );
};

export default Login;



