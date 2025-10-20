import React, { useState } from 'react';
import { Form, Input, Button, Card, Typography, message, Space } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined, UserAddOutlined } from '@ant-design/icons';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import styled from 'styled-components';

const { Title, Text } = Typography;

const RegisterContainer = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const RegisterCard = styled(Card)`
  width: 100%;
  max-width: 450px;
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

const Register = () => {
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);
    
    try {
      const result = await register(values.username, values.email, values.password);
      
      if (result.success) {
        message.success('Inscription réussie ! Veuillez vous connecter.');
        navigate('/login');
      } else {
        message.error(result.error);
      }
    } catch (error) {
      message.error('Erreur lors de l\'inscription');
    } finally {
      setLoading(false);
    }
  };

  return (
    <RegisterContainer>
      <RegisterCard>
        <StyledTitle level={2}>
          <UserAddOutlined /> Inscription
        </StyledTitle>
        
        <Form
          name="register"
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
                message: 'Veuillez saisir un nom d\'utilisateur !',
              },
              {
                min: 3,
                message: 'Le nom d\'utilisateur doit contenir au moins 3 caractères !',
              },
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="Nom d'utilisateur"
            />
          </Form.Item>

          <Form.Item
            name="email"
            label="Email"
            rules={[
              {
                required: true,
                message: 'Veuillez saisir votre email !',
              },
              {
                type: 'email',
                message: 'Veuillez saisir un email valide !',
              },
            ]}
          >
            <Input
              prefix={<MailOutlined />}
              placeholder="email@exemple.com"
            />
          </Form.Item>

          <Form.Item
            name="password"
            label="Mot de passe"
            rules={[
              {
                required: true,
                message: 'Veuillez saisir un mot de passe !',
              },
              {
                min: 8,
                message: 'Le mot de passe doit contenir au moins 8 caractères !',
              },
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Mot de passe"
            />
          </Form.Item>

          <Form.Item
            name="confirmPassword"
            label="Confirmer le mot de passe"
            dependencies={['password']}
            rules={[
              {
                required: true,
                message: 'Veuillez confirmer votre mot de passe !',
              },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('Les mots de passe ne correspondent pas !'));
                },
              }),
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Confirmer le mot de passe"
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
              S'inscrire
            </Button>
          </Form.Item>
        </Form>

        <Space direction="vertical" style={{ width: '100%', textAlign: 'center' }}>
          <Text>
            Déjà un compte ?{' '}
            <Link to="/login" style={{ color: '#1890ff', fontWeight: '600' }}>
              Se connecter
            </Link>
          </Text>
        </Space>
      </RegisterCard>
    </RegisterContainer>
  );
};

export default Register;





