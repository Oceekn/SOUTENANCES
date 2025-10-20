import React, { useState, useEffect } from 'react';
import { Form, Input, Button, Card, Typography, Alert, message, Space } from 'antd';
import { LockOutlined, EyeInvisibleOutlined, EyeTwoTone, CheckCircleOutlined, MailOutlined } from '@ant-design/icons';
import { useParams, useNavigate, Link } from 'react-router-dom';
import styled from 'styled-components';
import axios from 'axios';

const { Title, Text, Paragraph } = Typography;
const { Password } = Input;

const ResetPasswordContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  
  .reset-password-card {
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
  
  .password-strength {
    margin-top: 8px;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 12px;
    
    &.weak {
      background: #fff2f0;
      border: 1px solid #ffccc7;
      color: #cf1322;
    }
    
    &.medium {
      background: #fff7e6;
      border: 1px solid #ffd591;
      color: #d46b08;
    }
    
    &.strong {
      background: #f6ffed;
      border: 1px solid #b7eb8f;
      color: #389e0d;
    }
  }
`;

const ResetPassword = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [passwordReset, setPasswordReset] = useState(false);
  const [error, setError] = useState(null);
  const [tokenValid, setTokenValid] = useState(true);
  const [passwordStrength, setPasswordStrength] = useState('weak');
  
  const { token } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    // Vérifier la validité du token
    validateToken();
  }, [token]);

  const validateToken = async () => {
    try {
      await axios.post('/api/users/validate-reset-token/', { token });
      setTokenValid(true);
    } catch (error) {
      setTokenValid(false);
      setError('Le lien de réinitialisation est invalide ou a expiré');
    }
  };

  const checkPasswordStrength = (password) => {
    let score = 0;
    
    if (password.length >= 8) score++;
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    
    if (score <= 2) return 'weak';
    if (score <= 3) return 'medium';
    return 'strong';
  };

  const onFinish = async (values) => {
    if (values.newPassword !== values.confirmPassword) {
      message.error('Les mots de passe ne correspondent pas');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('/api/users/reset-password/', {
        token: token,
        new_password: values.newPassword,
        email: values.email
      });
      
      if (response.status === 200) {
        setPasswordReset(true);
        message.success('Mot de passe réinitialisé avec succès !');
        
        // Rediriger vers la connexion après 3 secondes
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      }
    } catch (error) {
      console.error('Erreur lors de la réinitialisation:', error);
      
      if (error.response?.data?.error) {
        setError(error.response.data.error);
      } else if (error.response?.status === 400) {
        setError('Le lien de réinitialisation est invalide ou a expiré');
      } else {
        setError('Erreur lors de la réinitialisation. Veuillez réessayer.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = (e) => {
    const password = e.target.value;
    const strength = checkPasswordStrength(password);
    setPasswordStrength(strength);
  };

  if (!tokenValid) {
    return (
      <ResetPasswordContainer>
        <Card className="reset-password-card">
          <div style={{ textAlign: 'center', padding: '24px' }}>
            <Alert
              message="Lien Invalide"
              description="Le lien de réinitialisation est invalide ou a expiré. Veuillez demander un nouveau lien."
              type="error"
              showIcon
              style={{ marginBottom: '24px' }}
            />
            
            <Link to="/forgot-password">
              <Button type="primary" block>
                Demander un nouveau lien
              </Button>
            </Link>
          </div>
        </Card>
      </ResetPasswordContainer>
    );
  }

  if (passwordReset) {
    return (
      <ResetPasswordContainer>
        <Card className="reset-password-card">
          <div className="success-message">
            <CheckCircleOutlined style={{ fontSize: '48px', color: '#52c41a', marginBottom: '16px' }} />
            <Title level={3} style={{ color: '#52c41a', marginBottom: '16px' }}>
              Mot de Passe Réinitialisé !
            </Title>
            <Paragraph style={{ fontSize: '16px', marginBottom: '24px' }}>
              Votre mot de passe a été modifié avec succès. 
              Vous allez être redirigé vers la page de connexion.
            </Paragraph>
            
            <Alert
              message="Redirection"
              description="Redirection automatique vers la page de connexion dans quelques secondes..."
              type="info"
              showIcon
            />
          </div>
        </Card>
      </ResetPasswordContainer>
    );
  }

  return (
    <ResetPasswordContainer>
      <Card className="reset-password-card">
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <Title level={2} style={{ color: '#1890ff', marginBottom: '8px' }}>
            Nouveau Mot de Passe
          </Title>
          <Text type="secondary">
            Choisissez un nouveau mot de passe sécurisé
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
          name="resetPassword"
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
          
          <Form.Item
            name="newPassword"
            label="Nouveau Mot de Passe"
            rules={[
              { required: true, message: 'Veuillez entrer un nouveau mot de passe' },
              { min: 8, message: 'Le mot de passe doit contenir au moins 8 caractères' },
              { 
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 
                message: 'Le mot de passe doit contenir au moins une minuscule, une majuscule et un chiffre' 
              }
            ]}
          >
            <Password
              prefix={<LockOutlined />}
              placeholder="Nouveau mot de passe"
              size="large"
              onChange={handlePasswordChange}
              iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
            />
          </Form.Item>

          {form.getFieldValue('newPassword') && (
            <div className={`password-strength ${passwordStrength}`}>
              Force du mot de passe : {passwordStrength === 'weak' ? 'Faible' : passwordStrength === 'medium' ? 'Moyenne' : 'Forte'}
            </div>
          )}

          <Form.Item
            name="confirmPassword"
            label="Confirmer le Mot de Passe"
            rules={[
              { required: true, message: 'Veuillez confirmer le mot de passe' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('newPassword') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('Les mots de passe ne correspondent pas'));
                },
              }),
            ]}
          >
            <Password
              prefix={<LockOutlined />}
              placeholder="Confirmer le mot de passe"
              size="large"
              iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
              size="large"
              icon={<LockOutlined />}
            >
              {loading ? 'Réinitialisation...' : 'Réinitialiser le mot de passe'}
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
    </ResetPasswordContainer>
  );
};

export default ResetPassword;


