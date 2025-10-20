import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Layout, Card, Row, Col, message, Spin, Alert, Button, Space, Progress, Divider } from 'antd';
import { ReloadOutlined, PlayCircleOutlined, BarChartOutlined, DownloadOutlined, HistoryOutlined } from '@ant-design/icons';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';

import FileUpload from './FileUpload';
import SimulationForm from './SimulationForm';
import SimulationResults from './SimulationResults';
import RiskCalculator from './RiskCalculator';
import DataPreview from './DataPreview';

const { Content } = Layout;

// Animations CSS
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const slideIn = keyframes`
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const DashboardContainer = styled.div`
  padding: 24px;
  background: #f0f2f5;
  min-height: 100vh;
  animation: ${fadeIn} 0.6s ease-out;
`;

const DashboardHeader = styled.div`
  margin-bottom: 24px;
  text-align: center;
  animation: ${slideIn} 0.8s ease-out;
`;

const DashboardTitle = styled.h1`
  color: #1890ff;
  margin-bottom: 8px;
`;

const DashboardSubtitle = styled.p`
  color: #666;
  font-size: 16px;
  margin: 0;
`;

const AnimatedCard = styled(Card)`
  transition: all 0.3s ease;
  animation: ${fadeIn} 0.6s ease-out;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  }
`;

const ProgressContainer = styled.div`
  margin: 16px 0;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
  
  .ant-progress-text {
    color: white !important;
    font-weight: bold;
  }
`;

const SimulationStatus = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 16px 0;
  padding: 16px;
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  border-radius: 8px;
  animation: ${fadeIn} 0.5s ease-out;
`;

const Dashboard = () => {
  const [lendingFile, setLendingFile] = useState(null);
  const [recoveryFile, setRecoveryFile] = useState(null);
  const [currentSimulation, setCurrentSimulation] = useState(null);
  const [simulationResults, setSimulationResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [simulationStep, setSimulationStep] = useState('');
  const monitoringRef = useRef(null); // Référence pour le monitoring

  // Configuration axios avec token d'authentification
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Token ${token}`;
    }
  }, []);


  // Nettoyage du monitoring lors du démontage du composant
  useEffect(() => {
    return () => {
      // Nettoyer les timeouts et arrêter le monitoring
      if (monitoringRef.current && typeof monitoringRef.current === 'function') {
        monitoringRef.current();
        monitoringRef.current = null;
      }
      // Nettoyage du composant
    };
  }, []);

  const handleFilesUploaded = useCallback((files) => {
    if (files && files.lending && files.recovery) {
      setLendingFile(files.lending);
      setRecoveryFile(files.recovery);
      message.success('Fichiers prêts pour la simulation !');
      
      // Réinitialiser les résultats précédents
      setCurrentSimulation(null);
      setSimulationResults(null);
      setError(null);
      setProgress(0);
    }
  }, []);

  const fetchSimulationResults = async (simulationId) => {
    try {
      console.log('🔄 Récupération des résultats pour simulation:', simulationId);
      const response = await axios.get(`/api/simulations/${simulationId}/results/`);
      console.log('✅ Résultats reçus:', response.data);
      setSimulationResults(response.data);
      message.success('Simulation terminée ! Résultats disponibles.');
    } catch (error) {
      console.error('❌ Erreur lors de la récupération des résultats:', error);
      console.error('❌ Détails de l\'erreur:', error.response?.data);
      setError(`Erreur lors de la récupération des résultats: ${error.response?.data?.detail || error.message}`);
    }
  };

  const monitorSimulationStatus = async (simulationId) => {
    let isMonitoring = true; // Flag pour arrêter le monitoring
    
    const checkStatus = async () => {
      if (!isMonitoring) return; // Arrêter si le flag est false
      
      try {
        const response = await axios.get(`/api/simulations/${simulationId}/status/`);
        const status = response.data.status;
        
        if (status === 'completed') {
          isMonitoring = false; // Arrêter le monitoring
          setProgress(100);
          setSimulationStep('Simulation terminée !');
          // Récupérer les résultats complets
          await fetchSimulationResults(simulationId);
          setLoading(false);
        } else if (status === 'failed') {
          isMonitoring = false; // Arrêter le monitoring
          setError('La simulation a échoué');
          setLoading(false);
          setProgress(0);
        } else if (status === 'running') {
          // Progression stable sans Math.random()
          setProgress(prev => {
            const increment = 5; // Incrément fixe
            const newProgress = Math.min(prev + increment, 85);
            return newProgress;
          });
          setSimulationStep('Calcul en cours...');
          // Continuer à surveiller seulement si toujours en cours
          if (isMonitoring) {
            setTimeout(checkStatus, 5000); // Augmenter l'intervalle à 5 secondes
          }
        }
      } catch (error) {
        console.error('Erreur lors de la vérification du statut:', error);
        if (isMonitoring) {
          setTimeout(checkStatus, 5000);
        }
      }
    };

    checkStatus();
    
    // Retourner une fonction pour arrêter le monitoring
    return () => {
      isMonitoring = false;
    };
  };

  const handleSimulationStarted = useCallback(async (simulation) => {
    if (!simulation.id) {
      setError('Erreur: ID de simulation manquant');
      return;
    }
    
    setCurrentSimulation(simulation);
    setLoading(true);
    setError(null);
    setProgress(0);
    setSimulationStep('Initialisation...');
    
    // Commencer à surveiller le statut de la simulation
    const stopMonitoring = monitorSimulationStatus(simulation.id);
    monitoringRef.current = stopMonitoring;
  }, []);

  const handleReloadSimulation = useCallback(async () => {
    if (!currentSimulation) return;
    
    try {
      setLoading(true);
      setError(null);
      setProgress(0);
      setSimulationStep('Relancement...');
      
      // Relancer la simulation
      const response = await axios.post(`/api/simulations/`, {
        method: currentSimulation.method,
        num_samples: currentSimulation.num_samples,
        alpha: currentSimulation.alpha,
        lending_file: lendingFile,
        recovery_file: recoveryFile
      }, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      const newSimulation = response.data;
      setCurrentSimulation(newSimulation);
      
      // Surveiller le nouveau statut
      const stopMonitoring = monitorSimulationStatus(newSimulation.id);
      monitoringRef.current = stopMonitoring;
      
    } catch (error) {
      setError('Erreur lors du relancement de la simulation');
      setLoading(false);
    }
  }, [currentSimulation, lendingFile, recoveryFile]);

  const handleClearResults = useCallback(() => {
    setCurrentSimulation(null);
    setSimulationResults(null);
    setError(null);
    setLoading(false);
    setProgress(0);
    setSimulationStep('');
  }, []);

  const getDashboardStatus = () => {
    if (error) {
      return (
        <Alert
          message="Erreur"
          description={error}
          type="error"
          showIcon
          action={
            <Button size="small" onClick={handleClearResults}>
              Effacer
            </Button>
          }
        />
      );
    }

    if (loading) {
      return (
        <div>
          <SimulationStatus>
            <PlayCircleOutlined style={{ fontSize: '24px', color: '#52c41a' }} />
            <div>
              <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
                {simulationStep}
              </div>
              <Progress 
                percent={Math.round(progress)} 
                status="active" 
                strokeColor={{
                  '0%': '#108ee9',
                  '100%': '#87d068',
                }}
                style={{ width: 200 }}
              />
            </div>
          </SimulationStatus>
        </div>
      );
    }

    if (simulationResults) {
      return (
        <Alert
          message="Simulation terminée"
          description="Résultats disponibles ci-dessous"
          type="success"
          showIcon
          action={
            <Space>
              <Button 
                size="small" 
                icon={<ReloadOutlined />}
                onClick={handleReloadSimulation}
              >
                Relancer
              </Button>
              <Button 
                size="small" 
                onClick={handleClearResults}
              >
                Nouvelle simulation
              </Button>
            </Space>
          }
        />
      );
    }

    if (lendingFile && recoveryFile) {
      return (
        <Alert
          message="Fichiers prêts"
          description="Vous pouvez maintenant configurer et lancer la simulation"
          type="success"
          showIcon
        />
      );
    }

    return (
      <Alert
        message="Prêt pour la simulation"
        description="Commencez par uploader vos fichiers CSV"
        type="info"
        showIcon
      />
    );
  };

  return (
    <Layout>
      <Content>
        <DashboardContainer>
          <DashboardHeader>
            <DashboardTitle>📊 Tableau de Bord d'Analyse de Risque de Crédit</DashboardTitle>
            <DashboardSubtitle>
              Simulation Monte Carlo et Bootstrap pour le calcul des provisions
            </DashboardSubtitle>
          </DashboardHeader>

          {/* Statut global */}
          <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
            <Col span={24}>
              {getDashboardStatus()}
            </Col>
          </Row>

          {/* Upload des fichiers */}
          <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
            <Col span={24}>
              <AnimatedCard>
                <FileUpload onFilesUploaded={handleFilesUploaded} />
              </AnimatedCard>
            </Col>
          </Row>

          {/* Configuration et lancement de simulation */}
          <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
            <Col span={24}>
              <AnimatedCard>
                <SimulationForm
                  lendingFile={lendingFile}
                  recoveryFile={recoveryFile}
                  onSimulationStarted={handleSimulationStarted}
                />
              </AnimatedCard>
            </Col>
          </Row>

          {/* Aperçu des données */}
          {lendingFile && recoveryFile && (
            <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
              <Col span={24}>
                <AnimatedCard>
                  <DataPreview
                    lendingFile={lendingFile}
                    recoveryFile={recoveryFile}
                  />
                </AnimatedCard>
              </Col>
            </Row>
          )}

          {/* Résultats de simulation */}
          {simulationResults && (
            <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
              <Col span={24}>
                <AnimatedCard>
                  <SimulationResults
                    results={simulationResults}
                    onReload={handleReloadSimulation}
                  />
                </AnimatedCard>
              </Col>
            </Row>
          )}

          {/* Calculateur de risque */}
          {simulationResults && (
            <Row gutter={[16, 16]}>
              <Col span={24}>
                <AnimatedCard>
                  <RiskCalculator simulationResults={simulationResults} />
                </AnimatedCard>
              </Col>
            </Row>
          )}

          {/* Indicateurs de performance */}
          <Row gutter={[16, 16]} style={{ marginTop: '24px' }}>
            <Col span={8}>
              <AnimatedCard size="small" title="📁 Fichiers">
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1890ff' }}>
                    {lendingFile && recoveryFile ? '2/2' : '0/2'}
                  </div>
                  <div style={{ color: '#666' }}>Fichiers CSV</div>
                </div>
              </AnimatedCard>
            </Col>
            <Col span={8}>
              <AnimatedCard size="small" title="🎯 Simulations">
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#52c41a' }}>
                    {currentSimulation ? '1' : '0'}
                  </div>
                  <div style={{ color: '#666' }}>En cours</div>
                </div>
              </AnimatedCard>
            </Col>
            <Col span={8}>
              <AnimatedCard size="small" title="📊 Résultats">
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#722ed1' }}>
                    {simulationResults ? '1' : '0'}
                  </div>
                  <div style={{ color: '#666' }}>Disponibles</div>
                </div>
              </AnimatedCard>
            </Col>
          </Row>
        </DashboardContainer>
      </Content>
    </Layout>
  );
};

export default Dashboard;
