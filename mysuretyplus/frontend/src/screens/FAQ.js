import React from 'react';
import { Button, Typography, Collapse } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const { Title } = Typography;
const { Panel } = Collapse;

const FAQ = () => {
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
        paddingTop: '80px'
      }}>
        <Title level={1} style={{ color: 'white', textAlign: 'center', marginBottom: '40px' }}>
          Questions Fréquemment Posées
        </Title>
        
        <Collapse
          ghost
          style={{
            background: 'rgba(255, 255, 255, 0.1)',
            borderRadius: '8px'
          }}
        >
          <Panel header="Qu'est-ce que MySuretyPlus ?" key="1">
            <p style={{ color: 'rgba(255, 255, 255, 0.9)' }}>
              MySuretyPlus est une application web d'analyse de risque de crédit qui utilise des simulations 
              Monte Carlo et Bootstrap pour calculer les provisions nécessaires.
            </p>
          </Panel>
          
          <Panel header="Comment fonctionne le calcul de provision ?" key="2">
            <p style={{ color: 'rgba(255, 255, 255, 0.9)' }}>
              La provision est calculée comme le maximum de la somme cumulée des transactions 
              (emprunts moins remboursements) sur une période donnée.
            </p>
          </Panel>
          
          <Panel header="Quelle est la différence entre Monte Carlo et Bootstrap ?" key="3">
            <p style={{ color: 'rgba(255, 255, 255, 0.9)' }}>
              Monte Carlo génère des échantillons aléatoires basés sur des distributions statistiques, 
              tandis que Bootstrap rééchantillonne les données existantes avec remplacement.
            </p>
          </Panel>
          
          <Panel header="Puis-je importer mes propres données ?" key="4">
            <p style={{ color: 'rgba(255, 255, 255, 0.9)' }}>
              Oui, vous pouvez importer des fichiers CSV contenant vos données d'emprunts et de remboursements 
              pour effectuer des analyses personnalisées.
            </p>
          </Panel>
          
          <Panel header="L'application est-elle sécurisée ?" key="5">
            <p style={{ color: 'rgba(255, 255, 255, 0.9)' }}>
              Absolument. Toutes les données sont traitées de manière sécurisée et les utilisateurs 
              doivent s'authentifier pour accéder à l'application.
            </p>
          </Panel>
        </Collapse>
      </div>
    </div>
  );
};

export default FAQ;

