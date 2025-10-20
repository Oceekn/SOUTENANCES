import React, { useState } from 'react';
import { Form, Input, Button, Card, Typography, Alert, message, Space } from 'antd';
import { MailOutlined, ArrowLeftOutlined, CheckCircleOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import axios from 'axios';

const { Title, Text, Paragraph } = Typography;

const ForgotPasswordContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  
  .forgot-password-card {
    width: 100%;
    max-width: 400px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border-radius: 12px;
  }
  
  .ant-form-item {
    margin-bottom: 20px;
  }
  
  .ant-btn {
    height: 45px;
    border-radius: 8px;
    font-weight: 600;
  }
  
  .success-message {
    text-align: center;
    padding: 24px;
  }
  
  .back-link {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #1890ff;
    text-decoration: none;
    margin-bottom: 16px;
    
    &:hover {
      color: #40a9ff;
    }
  }
`;

const ForgotPassword = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);
  const [error, setError] = useState(null);

  const onFinish = async (values) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('/api/users/forgot-password/', {
        email: values.email
      });
      
      if (response.status === 200) {
        setEmailSent(true);
        message.success('Email de réinitialisation envoyé avec succès !');
      }
    } catch (error) {
      console.error('Erreur lors de la demande de réinitialisation:', error);
      
      if (error.response?.data?.error) {
        setError(error.response.data.error);
      } else if (error.response?.status === 404) {
        setError('Aucun compte trouvé avec cette adresse email');
      } else {
        setError('Erreur lors de l\'envoi de l\'email. Veuillez réessayer.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleBackToLogin = () => {
    setEmailSent(false);
    setError(null);
    form.resetFields();
  };

  if (emailSent) {
    return (
      <ForgotPasswordContainer>
        <Card className="forgot-password-card">
          <div className="success-message">
            <CheckCircleOutlined style={{ fontSize: '48px', color: '#52c41a', marginBottom: '16px' }} />
            <Title level={3} style={{ color: '#52c41a', marginBottom: '16px' }}>
              Email Envoyé !
            </Title>
            <Paragraph style={{ fontSize: '16px', marginBottom: '24px' }}>
              Nous avons envoyé un lien de réinitialisation à votre adresse email.
              Veuillez vérifier votre boîte de réception et suivre les instructions.
            </Paragraph>
            
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <Alert
                message="Important"
                description="Le lien expire dans 1 heure. Si vous ne recevez pas l'email, vérifiez vos spams."
                type="info"
                showIcon
              />
              
              <Button 
                type="primary" 
                block 
                onClick={handleBackToLogin}
                icon={<ArrowLeftOutlined />}
              >
                Retour à la connexion
              </Button>
            </Space>
          </div>
        </Card>
      </ForgotPasswordContainer>
    );
  }

  return (
    <ForgotPasswordContainer>
      <Card className="forgot-password-card">
        <Link to="/login" className="back-link">
          <ArrowLeftOutlined />
          Retour à la connexion
        </Link>
        
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <Title level={2} style={{ color: '#1890ff', marginBottom: '8px' }}>
            Mot de Passe Oublié ?
          </Title>
          <Text type="secondary">
            Entrez votre adresse email pour recevoir un lien de réinitialisation
          </Text>
        </div>

        {error && (
          <Alert
            message="Erreur"
            description={error}
            type="error"
            showIcon
            style={{ marginBottom: '24px' }}
          />
        )}

        <Form
          form={form}
          name="forgotPassword"
          onFinish={onFinish}
          layout="vertical"
        >
          <Form.Item
            name="email"
            label="Adresse Email"
            rules={[
              { required: true, message: 'Veuillez entrer votre adresse email' },
              { type: 'email', message: 'Veuillez entrer une adresse email valide' }
            ]}
          >
            <Input
              prefix={<MailOutlined />}
              placeholder="votre@email.com"
              size="large"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
              size="large"
              icon={<MailOutlined />}
            >
              {loading ? 'Envoi en cours...' : 'Envoyer le lien de réinitialisation'}
            </Button>
          </Form.Item>
        </Form>

        <div style={{ textAlign: 'center', marginTop: '24px' }}>
          <Text type="secondary">
            Vous vous souvenez de votre mot de passe ?{' '}
            <Link to="/login" style={{ color: '#1890ff' }}>
              Se connecter
            </Link>
          </Text>
        </div>
      </Card>
    </ForgotPasswordContainer>
  );
};

export default ForgotPassword;


