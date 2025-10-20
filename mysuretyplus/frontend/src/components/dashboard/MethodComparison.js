import React, { useState } from 'react';
import { Card, Row, Col, Button, Progress, Alert, Space, Typography, Divider, message } from 'antd';
import { PlayCircleOutlined, BarChartOutlined, ReloadOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import axios from 'axios';

const { Title, Text } = Typography;

const ComparisonContainer = styled.div`
  .method-card {
    transition: all 0.3s ease;
    border: 2px solid transparent;
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    &.active {
      border-color: #1890ff;
      background: #f0f8ff;
    }
    
    &.completed {
      border-color: #52c41a;
      background: #f6ffed;
    }
  }
  
  .method-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
  }
  
  .method-icon {
    font-size: 24px;
    padding: 12px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .monte-carlo-icon {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }
  
  .bootstrap-icon {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
  }
  
  .results-section {
    margin-top: 16px;
    padding: 16px;
    background: #fafafa;
    border-radius: 8px;
  }
`;

const MethodComparison = ({ lendingFile, recoveryFile }) => {
  const [monteCarloStatus, setMonteCarloStatus] = useState('idle'); // idle, running, completed, error
  const [bootstrapStatus, setBootstrapStatus] = useState('idle');
  const [monteCarloProgress, setMonteCarloProgress] = useState(0);
  const [bootstrapProgress, setBootstrapProgress] = useState(0);
  const [monteCarloResults, setMonteCarloResults] = useState(null);
  const [bootstrapResults, setBootstrapResults] = useState(null);
  const [comparisonResults, setComparisonResults] = useState(null);

  const runMonteCarlo = async () => {
    if (!lendingFile || !recoveryFile) {
      message.error('Veuillez d\'abord télécharger les fichiers de données');
      return;
    }

    setMonteCarloStatus('running');
    setMonteCarloProgress(0);
    
    try {
      const token = localStorage.getItem('token');
      const formData = new FormData();
      formData.append('lending_file', lendingFile);
      formData.append('recovery_file', recoveryFile);
      formData.append('num_samples', 1000);
      formData.append('method', 'montecarlo');
      formData.append('alpha', 0.95);

      const startTime = Date.now();
      
      const response = await axios.post('/api/simulations/', formData, {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      const simulationId = response.data.id;
      
      // Surveiller la progression
      const checkProgress = async () => {
        try {
          const statusResponse = await axios.get(`/api/simulations/${simulationId}/status/`, {
            headers: { 'Authorization': `Token ${token}` }
          });
          
          if (statusResponse.data.status === 'completed') {
            setMonteCarloProgress(100);
            setMonteCarloStatus('completed');
            
            const resultsResponse = await axios.get(`/api/simulations/${simulationId}/results/`, {
              headers: { 'Authorization': `Token ${token}` }
            });
            
            const executionTime = (Date.now() - startTime) / 1000;
            setMonteCarloResults({
              method: 'Monte Carlo',
              provision: resultsResponse.data.real_provision,
              confidence_interval: [
                resultsResponse.data.confidence_interval.lower,
                resultsResponse.data.confidence_interval.upper
              ],
              execution_time: executionTime,
              simulation_id: simulationId
            });
          } else if (statusResponse.data.status === 'running') {
            setMonteCarloProgress(prev => Math.min(prev + 10, 90));
            setTimeout(checkProgress, 1000);
          } else if (statusResponse.data.status === 'failed') {
            setMonteCarloStatus('error');
            message.error('Erreur lors de la simulation Monte Carlo');
          }
        } catch (error) {
          setMonteCarloStatus('error');
          message.error('Erreur lors de la vérification du statut');
        }
      };
      
      setTimeout(checkProgress, 1000);
      
    } catch (error) {
      setMonteCarloStatus('error');
      message.error('Erreur lors du lancement de la simulation Monte Carlo');
    }
  };

  const runBootstrap = async () => {
    if (!lendingFile || !recoveryFile) {
      message.error('Veuillez d\'abord télécharger les fichiers de données');
      return;
    }

    setBootstrapStatus('running');
    setBootstrapProgress(0);
    
    try {
      const token = localStorage.getItem('token');
      const formData = new FormData();
      formData.append('lending_file', lendingFile);
      formData.append('recovery_file', recoveryFile);
      formData.append('num_samples', 1000);
      formData.append('method', 'bootstrap');
      formData.append('alpha', 0.95);

      const startTime = Date.now();
      
      const response = await axios.post('/api/simulations/', formData, {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      const simulationId = response.data.id;
      
      // Surveiller la progression
      const checkProgress = async () => {
        try {
          const statusResponse = await axios.get(`/api/simulations/${simulationId}/status/`, {
            headers: { 'Authorization': `Token ${token}` }
          });
          
          if (statusResponse.data.status === 'completed') {
            setBootstrapProgress(100);
            setBootstrapStatus('completed');
            
            const resultsResponse = await axios.get(`/api/simulations/${simulationId}/results/`, {
              headers: { 'Authorization': `Token ${token}` }
            });
            
            const executionTime = (Date.now() - startTime) / 1000;
            setBootstrapResults({
              method: 'Bootstrap',
              provision: resultsResponse.data.real_provision,
              confidence_interval: [
                resultsResponse.data.confidence_interval.lower,
                resultsResponse.data.confidence_interval.upper
              ],
              execution_time: executionTime,
              simulation_id: simulationId
            });
          } else if (statusResponse.data.status === 'running') {
            setBootstrapProgress(prev => Math.min(prev + 8, 90));
            setTimeout(checkProgress, 1000);
          } else if (statusResponse.data.status === 'failed') {
            setBootstrapStatus('error');
            message.error('Erreur lors de la simulation Bootstrap');
          }
        } catch (error) {
          setBootstrapStatus('error');
          message.error('Erreur lors de la vérification du statut');
        }
      };
      
      setTimeout(checkProgress, 1000);
      
    } catch (error) {
      setBootstrapStatus('error');
      message.error('Erreur lors du lancement de la simulation Bootstrap');
    }
  };

  const runBothMethods = async () => {
    try {
      await Promise.all([runMonteCarlo(), runBootstrap()]);
      
      // Attendre que les deux soient terminés
      const checkBothCompleted = () => {
        if (monteCarloResults && bootstrapResults) {
          const comparison = {
            monte_carlo: monteCarloResults,
            bootstrap: bootstrapResults,
            differences: {
              provision_diff: Math.abs(monteCarloResults.provision - bootstrapResults.provision),
              time_diff: Math.abs(monteCarloResults.execution_time - bootstrapResults.execution_time),
              precision: monteCarloResults.confidence_interval[1] - monteCarloResults.confidence_interval[0] < 
                        bootstrapResults.confidence_interval[1] - bootstrapResults.confidence_interval[0] ? 'Monte Carlo' : 'Bootstrap'
            }
          };
          setComparisonResults(comparison);
        } else {
          // Vérifier à nouveau dans 2 secondes
          setTimeout(checkBothCompleted, 2000);
        }
      };
      
      setTimeout(checkBothCompleted, 2000);
    } catch (error) {
      message.error('Erreur lors du lancement des deux méthodes');
    }
  };

  const resetComparison = () => {
    setMonteCarloStatus('idle');
    setBootstrapStatus('idle');
    setMonteCarloProgress(0);
    setBootstrapProgress(0);
    setMonteCarloResults(null);
    setBootstrapResults(null);
    setComparisonResults(null);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'idle': return '#d9d9d9';
      case 'running': return '#1890ff';
      case 'completed': return '#52c41a';
      case 'error': return '#ff4d4f';
      default: return '#d9d9d9';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'idle': return 'En attente';
      case 'running': return 'En cours';
      case 'completed': return 'Terminé';
      case 'error': return 'Erreur';
      default: return 'En attente';
    }
  };

  return (
    <ComparisonContainer>
      <Title level={3}>🔄 Comparaison des Méthodes</Title>
      <Text type="secondary">
        Comparez les performances des méthodes Monte Carlo et Bootstrap sur vos données
      </Text>

      <Divider />

      <Row gutter={[24, 24]}>
        {/* Monte Carlo */}
        <Col span={12}>
          <Card 
            className={`method-card ${monteCarloStatus === 'running' ? 'active' : monteCarloStatus === 'completed' ? 'completed' : ''}`}
            title={
              <div className="method-header">
                <div className="method-icon monte-carlo-icon">
                  🎲
                </div>
                <div>
                  <Title level={4} style={{ margin: 0 }}>Monte Carlo</Title>
                  <Text type="secondary">Génération aléatoire</Text>
                </div>
              </div>
            }
          >
            <div style={{ marginBottom: 16 }}>
              <Text strong>Statut: </Text>
              <Text style={{ color: getStatusColor(monteCarloStatus) }}>
                {getStatusText(monteCarloStatus)}
              </Text>
            </div>

            {monteCarloStatus === 'running' && (
              <Progress 
                percent={Math.round(monteCarloProgress)} 
                status="active" 
                strokeColor={{
                  '0%': '#667eea',
                  '100%': '#764ba2',
                }}
              />
            )}

            {monteCarloResults && (
              <div className="results-section">
                <Title level={5}>Résultats Monte Carlo</Title>
                <Row gutter={[8, 8]}>
                  <Col span={12}>
                    <Text strong>Provision:</Text>
                    <br />
                    <Text style={{ fontSize: '18px', color: '#1890ff' }}>
                      {monteCarloResults.provision.toFixed(2)} €
                    </Text>
                  </Col>
                  <Col span={12}>
                    <Text strong>Temps:</Text>
                    <br />
                    <Text>{monteCarloResults.execution_time.toFixed(1)}s</Text>
                  </Col>
                </Row>
              </div>
            )}

            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={runMonteCarlo}
              disabled={monteCarloStatus === 'running'}
              block
              style={{ marginTop: 16 }}
            >
              {monteCarloStatus === 'running' ? 'En cours...' : 'Lancer Monte Carlo'}
            </Button>
          </Card>
        </Col>

        {/* Bootstrap */}
        <Col span={12}>
          <Card 
            className={`method-card ${bootstrapStatus === 'running' ? 'active' : bootstrapStatus === 'completed' ? 'completed' : ''}`}
            title={
              <div className="method-header">
                <div className="method-icon bootstrap-icon">
                  🔄
                </div>
                <div>
                  <Title level={4} style={{ margin: 0 }}>Bootstrap</Title>
                  <Text type="secondary">Rééchantillonnage</Text>
                </div>
              </div>
            }
          >
            <div style={{ marginBottom: 16 }}>
              <Text strong>Statut: </Text>
              <Text style={{ color: getStatusColor(bootstrapStatus) }}>
                {getStatusText(bootstrapStatus)}
              </Text>
            </div>

            {bootstrapStatus === 'running' && (
              <Progress 
                percent={Math.round(bootstrapProgress)} 
                status="active" 
                strokeColor={{
                  '0%': '#f093fb',
                  '100%': '#f5576c',
                }}
              />
            )}

            {bootstrapResults && (
              <div className="results-section">
                <Title level={5}>Résultats Bootstrap</Title>
                <Row gutter={[8, 8]}>
                  <Col span={12}>
                    <Text strong>Provision:</Text>
                    <br />
                    <Text style={{ fontSize: '18px', color: '#f5576c' }}>
                      {bootstrapResults.provision.toFixed(2)} €
                    </Text>
                  </Col>
                  <Col span={12}>
                    <Text strong>Temps:</Text>
                    <br />
                    <Text>{bootstrapResults.execution_time.toFixed(1)}s</Text>
                  </Col>
                </Row>
              </div>
            )}

            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={runBootstrap}
              disabled={bootstrapStatus === 'running'}
              block
              style={{ marginTop: 16 }}
            >
              {bootstrapStatus === 'running' ? 'En cours...' : 'Lancer Bootstrap'}
            </Button>
          </Card>
        </Col>
      </Row>

      {/* Boutons de contrôle */}
      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col span={12}>
          <Button
            type="primary"
            size="large"
            icon={<PlayCircleOutlined />}
            onClick={runBothMethods}
            disabled={monteCarloStatus === 'running' || bootstrapStatus === 'running'}
            block
          >
            Lancer les Deux Méthodes
          </Button>
        </Col>
        <Col span={12}>
          <Button
            size="large"
            icon={<ReloadOutlined />}
            onClick={resetComparison}
            block
          >
            Réinitialiser
          </Button>
        </Col>
      </Row>

      {/* Résultats de comparaison */}
      {comparisonResults && (
        <Card style={{ marginTop: 24 }}>
          <Title level={4}>📊 Comparaison des Résultats</Title>
          <Row gutter={[24, 16]}>
            <Col span={8}>
              <div style={{ textAlign: 'center' }}>
                <Title level={3} style={{ color: '#1890ff' }}>
                  {comparisonResults.differences.provision_diff.toFixed(2)} €
                </Title>
                <Text>Différence de provision</Text>
              </div>
            </Col>
            <Col span={8}>
              <div style={{ textAlign: 'center' }}>
                <Title level={3} style={{ color: '#52c41a' }}>
                  {comparisonResults.differences.time_diff.toFixed(1)}s
                </Title>
                <Text>Différence de temps</Text>
              </div>
            </Col>
            <Col span={8}>
              <div style={{ textAlign: 'center' }}>
                <Title level={3} style={{ color: '#722ed1' }}>
                  {comparisonResults.differences.precision}
                </Title>
                <Text>Plus précis</Text>
              </div>
            </Col>
          </Row>
        </Card>
      )}
    </ComparisonContainer>
  );
};

export default MethodComparison;

