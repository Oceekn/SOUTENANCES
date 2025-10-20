import React from 'react';
import { Button, Typography } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const { Title, Paragraph } = Typography;

const About = () => {
  const navigate = useNavigate();

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px',
      color: 'white'
    }}>
      <Button
        icon={<ArrowLeftOutlined />}
        onClick={() => navigate('/')}
        style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          background: 'rgba(255, 255, 255, 0.2)',
          borderColor: 'rgba(255, 255, 255, 0.3)',
          color: 'white'
        }}
      >
        Retour
      </Button>

      <div style={{
        maxWidth: '800px',
        margin: '0 auto',
        paddingTop: '80px',
        textAlign: 'center'
      }}>
        <Title level={1} style={{ color: 'white', fontSize: '48px', marginBottom: '30px' }}>
          À Propos de MySuretyPlus
        </Title>
        
        <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', color: 'rgba(255, 255, 255, 0.9)' }}>
          MySuretyPlus est une application web révolutionnaire conçue pour aider les analystes financiers 
          à évaluer le risque de crédit de manière précise et efficace. Notre solution utilise des 
          simulations sophistiquées et des algorithmes d'intelligence artificielle pour calculer 
          les provisions nécessaires.
        </Paragraph>

        <Title level={2} style={{ color: 'white', marginTop: '40px' }}>
          Fonctionnalités Principales
        </Title>
        
        <ul style={{ textAlign: 'left', fontSize: '16px', color: 'rgba(255, 255, 255, 0.9)' }}>
          <li>Analyse de risque de crédit en temps réel</li>
          <li>Simulations Monte Carlo et Bootstrap</li>
          <li>Calcul automatique des provisions</li>
          <li>Visualisations interactives</li>
          <li>Interface utilisateur intuitive</li>
        </ul>
      </div>
    </div>
  );
};

export default About;

